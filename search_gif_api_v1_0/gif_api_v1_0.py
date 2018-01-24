from flask import Flask

from base import  CreateApp

app = CreateApp().create_app("production")
# app,sr= create_app()
if __name__ == '__main__':
    print(app.url_map)
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
