from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pass",
        database="blog"
    )
    return conn


@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)


@app.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE kullanici_id = %s", (user_id,))
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(posts)


@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT yorum FROM posts WHERE id = %s", (post_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(comments)


@app.route('/users/<int:user_id>/posts', methods=['POST'])
def add_post(user_id):
    new_post = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posts (baslik, aciklama, yorum, kullanici_id) VALUES (%s, %s, %s, %s)",
        (new_post['baslik'], new_post['aciklama'], new_post['yorum'], user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return 'Gönderi başarıyla eklendi!', 201


@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    new_comment = request.json['yorum']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE posts SET yorum = %s WHERE id = %s",
        (new_comment, post_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return 'Yorum başarıyla eklendi!', 201


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return 'Gönderi başarıyla silindi!', 204


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    updated_user = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET isim = %s, eposta = %s, meslek = %s WHERE id = %s",
        (updated_user['isim'], updated_user['eposta'], updated_user['meslek'], user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return 'Kullanıcı bilgileri başarıyla güncellendi!', 200

if __name__ == '__main__':
    app.run(debug=True)
