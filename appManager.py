from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask import send_file
from tigerdb import TigerDB
from tableRenderer import TableRenderer
import tempfile
import Uploader
from Apps import *
from jproperties import Properties

configs = Properties()
with open('app-config.properties', 'rb') as config_file:
    configs.load(config_file)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__, static_url_path='/static')
tiger = TigerDB(configs)
tableRenderer = TableRenderer()

@app.route('/views/<viewname>')
def viewByName(viewname):
    klass = globals()[viewname]
    viewer = klass()
    table = viewer.view(tiger, tableRenderer)
    return render_template('viewTemplate.html', title=viewer.getTitle(),
                           table=table, table_export_url=request.root_url + '/export/' + viewname)

@app.route('/export/<viewname>')
def exportByName(viewname):
    klass = globals()[viewname]
    viewer = klass()
    dataFrame = viewer.export(tiger)
    with tempfile.NamedTemporaryFile() as tempfilepath:
        dataFrame.to_csv(tempfilepath.name)
        return send_file(tempfilepath.name, as_attachment=True, download_name=viewname+".csv")

@app.route('/match/<resource>')
def match(resource):
    klass = globals()[resource]
    matcher = klass()
    table_needed, table_options = matcher.getTables(tiger, tableRenderer)
    return render_template('matchTemplate.html', Type=matcher.getVertextType(),
                           table_needed=table_needed, table_options=table_options)

@app.route('/resolve/<resource>')
def resolve(resource):
    klass = globals()[resource]
    matcher = klass()
    table_needed, table_options = matcher.getTables(tiger, tableRenderer)
    return render_template('resolveTemplate.html', Type=matcher.getVertextType(),
                           table_needed=table_needed, table_options=table_options)


@app.route('/match', methods=["POST"])
def matchInGraph():
    try:
        if request.method == 'POST':
            tiger.match(request.form['id1'], request.form['id2'])
            print('match ', request.form['id1'], request.form['id2'])
            success = 1
            return jsonify(success)
    except Exception as e:
        print(e)
    finally:
        pass

@app.route('/remove')
def remove():
  return render_template("removeTemplate.html")


@app.route('/removeById')
def removeById():
  print(request)
  print(request.args)
  id = int(request.args['name'])
  print(id)
  result = tiger.deleteVertex(id)
  print(result)
  if result:
      return render_template("done.html")
  else:
     return render_template("failure.html")


@app.route('/test')
def test():
    return render_template('match.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/update", methods=["POST", "GET"])
def update():
    try:
        if request.method == 'POST':
            tiger.update(request.form['id'], request.form['field'], request.form['value'], request.form['vertex_type'] )
            success = 1
        return jsonify(success)
    except Exception as e:
        print(e)
    finally:
        pass


@app.route('/upload')
def upload_file():
  return render_template('upload.html')

@app.route('/uploader', methods=["POST"])
def save_file():
    if request.method == 'POST':
        Uploader.upload_file(request, tiger)
        return render_template('done.html')


@app.route('/success')
def success():
    return render_template('done.html')


@app.route('/finalized_match')
def finalized_match():
       return render_template('finalized_match.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)