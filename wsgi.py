from spot import create_app


application = create_app(debug=False)


if __name__ == '__main__':
    application.run()

