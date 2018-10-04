from api.views import conn, app


if __name__ == '__main__':
    conn.create_tables()
    conn.make_admin()
    app.run() 
