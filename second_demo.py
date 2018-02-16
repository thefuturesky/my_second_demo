from flask import Flask,render_template,url_for,request,redirect,session
import config
from models import User,Question,Answer
from exts import db
from decorator import login_required
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)



@app.route('/')
def index():
    context={
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)


@app.route('/login/',methods = ['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone=request.form.get('telephone')
        password=request.form.get('password')
        user = User.query.filter(User.telephone==telephone , User.password==password).first()
        if user:
            session['user_id']=user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return "输入的密码或者账号不正确，请核对后再重新输入！"

@app.route('/regist/',methods = ['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user=User.query.filter(User.telephone==telephone).first()
        if user:
            return "该手机号码已经被注册，请更换手机号码再注册"
        else:
            if password1 != password2:
                return "两次密码输入不一致，请重新输入"
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/logout')
def logout():
    #del session('user_id')
    #session.clear()
    session.pop('user_id')
    return redirect(url_for('login'))

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method =='GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question = Question(title=title,content=content)
        question.author=user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))
@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model=Question.query.filter(Question.id==question_id).first()
    count = len(question_model.answers)
    return render_template('detail.html',question=question_model,count=count)


@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content=request.form.get('comment')
    question_id = request.form.get('question_id')
    question=Question.query.filter(Question.id==question_id).first()
    user_id=session.get("user_id")
    user=User.query.filter(User.id==user_id).first()
    answer=Answer(content=content)
    answer.author=user
    answer.question=question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/search/')
@login_required
def search():
    q=request.args.get('q')
    questions=Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by('-create_time')
    return render_template('index.html',questions=questions)

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id==user_id).first()
        if user:
            return {'user':user}
    else:
        return {}

if __name__ == '__main__':
    app.run()