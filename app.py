from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config.get('INSTANCE_PORT', 80), debug=False)
