# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# DB 기본 코드
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.username} {self.title} 추천 by {self.username}'

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    name = '서병렬'
    motto = "행복해서 웃는게 아니라 웃어서 행복합니다."

    context = {
        "name": name,
        "motto": motto,
    }
    return render_template('motto.html', data=context)

@app.route("/music/")
def music():
    songList = Song.query.all()
    return render_template('music.html', data = songList)

@app.route("/music/<username>/")
def render_music_filter(username):
    filterList = Song.query.filter_by(username=username).all()
    return render_template('music.html', data=filterList)


@app.route("/iloveyou/<name>/")
def iloveyou(name):
    motto = f"{name}야 난 너뿐이야!"

    context = {
        'name': name,
        'motto': motto,
    }
    return render_template('motto.html', data=context)


@app.route("/music/create/")
def music_create():
    # form 에서 보낸 데이터 받기
    username = request.args.get("username")
    title = request.args.get("title")
    artist = request.args.get("artist")
    image_url = request.args.get("image_url")

    # db에 저장 객체생성 -> 추가 -> 커밋
    song = Song(username=username, title=title, artist=artist, image_url=image_url)
    db.session.add(song) 
    db.session.commit()
    # redirect는 함수명으로 페이지 리다이렉트
    return redirect(url_for('render_music_filter', username=username))
    

@app.route("/music/delete/", methods=['POST'])
def music_delete():
    
    id = request.form.get('songId')
    print(id)
    deleteSong = Song.query.get(id)
    print(deleteSong)
    if deleteSong:
        db.session.delete(deleteSong)
        db.session.commit()
    
    return redirect(url_for('music'))

if __name__ == "__main__":
    app.run(debug=True)