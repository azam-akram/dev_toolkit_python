from openpyxl import Workbook

# Create a new workbook and select the active worksheet
new_workbook = Workbook()
new_sheet = new_workbook.active

# Add column headers
new_sheet['A1'] = 'Product'
new_sheet['B1'] = 'Price'
new_sheet['C1'] = 'Stock'

# Add some data
new_sheet.append(['Laptop', 899.99, 10])
new_sheet.append(['Mouse', 19.99, 150])
new_sheet.append(['Keyboard', 49.99, 85])

# Save the new workbook
new_workbook.save('c://Users/azam/work/python/github/dev_toolkit_python/excel-utils/products.xlsx')
