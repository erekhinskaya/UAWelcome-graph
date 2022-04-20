from io import StringIO

class ColumnInfo:
  editable = False
  boolean = False
  selector = False

class TableRenderer:

  def render_header(self, header):
    file_str = StringIO()
    file_str.write('<thead class="thead-light">\n')
    file_str.write('  <tr>\n')
    for i in range(len(header)):
      file_str.write('  <th scope="col">')
      file_str.write(header[i])
      file_str.write("</th>\n")
    file_str.write("  </tr>\n")
    file_str.write("</thead>\n")
    return file_str.getvalue()

  def add_editable_text(self, file_str, row, c, header, column_info, vertex_type, match_id = None):
    print('header: ' + header)
    print('str(row[0]): ' + str(row[0]))
    id = header + '_' + str(row[0]) + '_' + vertex_type # assuming id
    if column_info.selector:
      file_str.write('<input name="select" type="radio" class="selection" id="' + row[0] + '" value="' + str(match_id) + '">')
      return
    file_str.write("<div class='edit' >")
    file_str.write(str(row[c]))
    file_str.write("</div>\n")
    if column_info.boolean:
      file_str.write("  <select id = '" + id + "' class='txtedit' >")
      file_str.write("<option value = 'False' > False </option>")
      file_str.write("<option value = 'True' > True </option>")
      file_str.write("</select>")
    else:
      file_str.write("  <input type='text' class='txtedit' value='")
      file_str.write(str(row[c]))
      file_str.write("' id='")
      file_str.write(id)
      file_str.write("' >")

  #data includes headers
  def render_table(self, data, column_map, vertex_type, match_id = None):
    file_str = StringIO()
    file_str.write("<table id='data' class='table table-bordered table-hover'>")
    file_str.write(self.render_header(data[0]))
    for row in data[1:]:
      file_str.write("  <tr>")
      for c in range(len(row)):
        header = data[0][c]
        column_info = column_map[header]
        if not column_info.editable:
          file_str.write("  <td>")
          file_str.write(str(row[c]))
          file_str.write("</td>")
        else:
          #<td><div class='edit' > {{user.name}}</div>
          #<input type='text' class='txtedit' value='{{(user.name)}}' id='Name_{{user.id}}' ></td>
          file_str.write("  <td>")
          self.add_editable_text(file_str, row, c, header, column_info, vertex_type, match_id)
          file_str.write("</td>\n")
      file_str.write("  </tr>")
    file_str.write("</table>")
    return file_str.getvalue()
