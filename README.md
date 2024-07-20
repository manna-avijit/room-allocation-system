# Room Allocation System

## Overview

The Room Allocation System is a web application designed to automate the process of assigning hostel rooms to groups. The application allows users to upload two CSV files: one containing group information and the other containing hostel information. The system allocates rooms based on group requirements, gender-specific accommodations, and room capacities.

## Features

- **Upload CSV Files**: Upload Group Information and Hostel Information CSV files.
- **Automatic Room Allocation**: Allocate rooms based on group ID, gender, and room capacity.
- **Download Results**: Obtain a CSV file with detailed room allocation results.

## CSV File Formats

### 1. Group Information CSV

Contains details about the groups needing accommodation.

- **Columns**:
  - `Group ID`: Unique identifier for each group.
  - `Members`: Number of members in the group.
  - `Gender`: Gender of the group members (e.g., Boys, Girls, or a combination like "5 Boys & 3 Girls").

**Example**:

| Group ID | Members | Gender         |
|----------|---------|----------------|
| 101      | 3       | Boys           |
| 102      | 4       | Girls          |
| 103      | 2       | Boys           |
| 104      | 5       | Girls          |
| 105      | 8       | 5 Boys & 3 Girls |


### 2. Hostel Information CSV

Contains details about available hostel rooms.

- **Columns**:
  - `Hostel Name`: Name of the hostel.
  - `Room Number`: Number of the room within the hostel.
  - `Capacity`: Maximum number of members the room can accommodate.
  - `Gender`: Gender accommodation of the room (e.g., Boys, Girls).

**Example**:

| Hostel Name   | Room Number | Capacity | Gender |
|---------------|-------------|----------|--------|
| Boys Hostel A | 101         | 3        | Boys   |
| Boys Hostel A | 102         | 4        | Boys   |
| Girls Hostel B| 201         | 2        | Girls  |
| Girls Hostel B| 202         | 5        | Girls  |

#### 3. Output

- A display of the allocated rooms indicating which group members are in which room.
- A downloadable CSV file with the allocation details.

**Example Output:**

| Group ID | Hostel Name   | Room Number | Members Allocated |
|----------|---------------|-------------|-------------------|
| 101      | Boys Hostel A | 101         | 3                 |
| 102      | Girls Hostel B| 202         | 4                 |
| 103      | Boys Hostel A | 102         | 2                 |
| 104      | Girls Hostel B| 202         | 5                 |

## Project Structure

- **app.py**: Main application file containing routes and logic for room allocation.
- **templates/index.html**: HTML template for the frontend interface.
- **uploads/**: Directory for storing uploaded CSV files.


## Usage

1. **Access the Application**: Open the web application in your browser.
2. **Upload CSV Files**: Use the form on the homepage to upload the Group Information CSV and Hostel Information CSV files.
3. **Submit for Allocation**: Click the "Upload and Allocate" button to process the files and allocate rooms.
4. **View Results**: Once processed, view the allocation results on the page and download the allocation CSV file.

## Logical Implementation

1. **File Upload Validation**:
   - Ensure both files are uploaded and are in CSV format.
   - Verify that the CSV files contain the required columns.

2. **Data Processing**:
   - Read the CSV files into dataframes using `pandas`.
   - Sort hostels by capacity and gender.
   - Allocate rooms to groups while keeping members of the same group together and adhering to gender-specific accommodations.

3. **Allocation Algorithm**:
   - For each group, allocate members to available rooms based on gender and capacity.
   - Handle mixed-gender groups by splitting the allocation into boys' and girls' rooms.
   - Generate a detailed allocation report.

4. **Output**:
   - Display the room allocation results on the web page.
   - Provide a downloadable CSV file containing the allocation details.

## Error Handling

The application provides error handling for common issues such as missing files, invalid file formats, and incorrect CSV structures. Appropriate error messages are displayed to the user.

## Conclusion

The Room Allocation System streamlines the process of assigning hostel rooms to groups based on provided CSV files. It features an intuitive user interface and robust backend logic to ensure efficient and accurate room assignments.
