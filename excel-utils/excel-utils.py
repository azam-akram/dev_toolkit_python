import os
import pandas as pd

def read_nth_column(file_path: str, column_number: int):
	if not os.path.exists(file_path):
		print("Error: File does not exist.")
		return []
	
	try:
		df = pd.read_excel(file_path, engine='openpyxl')
		col_index = column_number - 1  # Convert to zero-based index

		if col_index < 0 or col_index >= len(df.columns):
			print("Error: Invalid column number.")
			return []

		return df.iloc[:, col_index].dropna().tolist()
	
	except Exception as e:
		print(f"Error reading Excel file: {e}")
		return []


def update_cell_value(file_path: str, column_number: int, row_number: int, new_value):
	"""
	Updates the value in the nth column and mth row of an Excel file.
	
	:param file_path: Path to the Excel file.
	:param column_number: The column number (1-based index).
	:param row_number: The row number (1-based index).
	:param new_value: The new value to insert.
	"""
	if not os.path.exists(file_path):
		print("Error: File does not exist.")
		return False
	
	try:
		df = pd.read_excel(file_path, engine='openpyxl')
		col_index = column_number - 1  # Convert to zero-based index
		row_index = row_number - 1  # Convert to zero-based index

		if col_index < 0 or col_index >= len(df.columns):
			print("Error: Invalid column number.")
			return False
		
		if row_index < 0 or row_index >= len(df):
			print("Error: Invalid row number.")
			return False

		df.iloc[row_index, col_index] = new_value  # Update the cell
		df.to_excel(file_path, index=False, engine='openpyxl')  # Save changes

		print(f"Successfully updated cell at row {row_number}, column {column_number} with '{new_value}'")
		return True

	except Exception as e:
		print(f"Error updating Excel file: {e}")
		return False


if __name__ == "__main__":
	file_path = os.path.abspath("excel-utils\Financial_Sample.xlsx")
	print("Using file path:", file_path)

	# Read a specific column
	column_number = 2
	values = read_nth_column(file_path, column_number)
	print(f"Column {column_number} values:", values)

	# Update a specific cell
	row_number = 3
	new_value = "Updated Value for Canda"
	update_cell_value(file_path, column_number, row_number, new_value)
