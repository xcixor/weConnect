"""Runs the application"""
import os

from app import create_app

app = create_app('default')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run('', port=port)