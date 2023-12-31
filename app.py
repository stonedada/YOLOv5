from flask import Flask, request, render_template, redirect, url_for
import predict
import os

app = Flask(__name__)

# 上传文件存储目录
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# 检查文件扩展名是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查是否有文件被上传
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # 如果用户没有选择文件，浏览器会提交一个空字段
        if file.filename == '':
            return redirect(request.url)

        # 如果文件合法
        if file and allowed_file(file.filename):
            # 保存文件到指定目录
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            print(filename)
            file.save("./uploads/"+file.filename)

            # 在这里可以添加处理上传文件的代码，例如调用深度学习模型进行图像分析
            predict.res("./uploads/"+file.filename)
            return redirect('/tl')

    return render_template('uploads.html')

@app.route('/tl', methods=['GET', 'POST'])
def tl_file():
    # 使用url_for生成静态文件的URL
    image_url = url_for('static', filename='img.jpg')
    return render_template('tl_res.html', image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
