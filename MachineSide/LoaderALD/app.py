from flask import Flask

UPLOAD_FOLDER = 'C:/Users/Tanat/Desktop/uploads'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB maximum size
