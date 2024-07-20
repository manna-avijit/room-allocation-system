from flask import Flask, request, render_template, send_file, jsonify
import pandas as pd
import os
import io

app = Flask(__name__)
# Configure the upload folder and maximum file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    # Render the main HTML page for file upload
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        # Check if both files are in the request
        if 'group_file' not in request.files or 'hostel_file' not in request.files:
            return jsonify({'error': 'Both files are required'}), 400

        group_file = request.files['group_file']
        hostel_file = request.files['hostel_file']

        # Check if both files have been selected
        if group_file.filename == '' or hostel_file.filename == '':
            return jsonify({'error': 'Both files must be selected'}), 400

        # Ensure both files are in CSV format
        if not (group_file.filename.endswith('.csv') and hostel_file.filename.endswith('.csv')):
            return jsonify({'error': 'Both files must be CSV format'}), 400

        # Read the CSV files into DataFrames
        group_df = pd.read_csv(group_file)
        hostel_df = pd.read_csv(hostel_file)

        # Validate the structure of the group file
        required_group_columns = ['Group ID', 'Members', 'Gender']
        if not all(col in group_df.columns for col in required_group_columns):
            return jsonify({'error': 'Invalid group file structure'}), 400

        # Validate the structure of the hostel file
        required_hostel_columns = ['Hostel Name', 'Room Number', 'Capacity', 'Gender']
        if not all(col in hostel_df.columns for col in required_hostel_columns):
            return jsonify({'error': 'Invalid hostel file structure'}), 400

        # Perform the room allocation
        allocation_df = allocate_rooms(group_df, hostel_df)

        # Convert the resulting DataFrame to CSV
        output = io.StringIO()
        allocation_df.to_csv(output, index=False)
        output.seek(0)

        # Send the CSV file as a download
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='room_allocation.csv'
        )

    except Exception as e:
        # Handle any errors that occur during processing
        return jsonify({'error': str(e)}), 500

def allocate_rooms(groups, hostels):
    # Initialize a list to store allocation results
    allocation = []

    # Separate hostels by gender and sort by room capacity
    boys_hostels = hostels[hostels['Gender'] == 'Boys'].sort_values('Capacity', ascending=False)
    girls_hostels = hostels[hostels['Gender'] == 'Girls'].sort_values('Capacity', ascending=False)

    # Convert DataFrames to lists of dictionaries for easier processing
    boys_rooms = boys_hostels.to_dict('records')
    girls_rooms = girls_hostels.to_dict('records')

    def allocate_to_hostel(group_id, members, rooms):
        allocated = 0
        for room in rooms:
            if members == 0:
                break
            # Determine how many members can be allocated to the current room
            available = min(members, room['Capacity'])
            if available > 0:
                allocation.append({
                    'Group ID': group_id,
                    'Hostel Name': room['Hostel Name'],
                    'Room Number': room['Room Number'],
                    'Members Allocated': available
                })
                # Update the room capacity and remaining members
                room['Capacity'] -= available
                members -= available
                allocated += available
        return allocated

    # Iterate through each group in the group DataFrame
    for _, group in groups.iterrows():
        group_id = group['Group ID']
        total_members = group['Members']
        gender = group['Gender']

        if '&' in str(gender):
            # Handle mixed gender groups
            boys_count = int(str(gender).split('&')[0].strip().split()[0])
            girls_count = total_members - boys_count

            boys_allocated = allocate_to_hostel(group_id, boys_count, boys_rooms)
            girls_allocated = allocate_to_hostel(group_id, girls_count, girls_rooms)
            
            unallocated = total_members - boys_allocated - girls_allocated
        elif 'Boys' in str(gender):
            # Allocate boys' groups
            allocated = allocate_to_hostel(group_id, total_members, boys_rooms)
            unallocated = total_members - allocated
        elif 'Girls' in str(gender):
            # Allocate girls' groups
            allocated = allocate_to_hostel(group_id, total_members, girls_rooms)
            unallocated = total_members - allocated
        else:
            unallocated = total_members

        # Add unallocated members to the results
        if unallocated > 0:
            allocation.append({
                'Group ID': group_id,
                'Hostel Name': 'Unallocated',
                'Room Number': 'N/A',
                'Members Allocated': unallocated
            })

    return pd.DataFrame(allocation)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)