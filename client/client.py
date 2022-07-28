from flask import Blueprint, render_template

client_bp = Blueprint(
    'client_bp',
    __name__,  # 'Client Blueprint'
    template_folder='templates',  # Required for our purposes
    static_folder='static',  # Again, this is required
    static_url_path='/client/static'  # Flask will be confused if you don't do this
)


@client_bp.route("/")
def index():
    return render_template("main.html")

#
# @client_bp.route("/challenge")
# def challenge():
#     return render_template("challenge.html")
