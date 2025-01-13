from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

"""
Configure using SQLite database for testing. Will move to cloud when ready.
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///research_papers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

"""
These are the columns in the database.
"""
class ResearchPaper(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_title = db.Column(db.String, nullable=False)
    authors = db.Column(db.String, nullable=False)
    contact_info = db.Column(db.String)
    year_published = db.Column(db.Integer)
    institution = db.Column(db.String)
    num_publications_used = db.Column(db.Integer)
    full_link = db.Column(db.String)
    shortened_link = db.Column(db.String)
    is_duplicate = db.Column(db.Boolean, default=False)
    qual_score_method = db.Column(db.String)
    study_type = db.Column(db.String)
    qualsyst_criteria = db.Column(db.String)


"""Creating the tables in the database."""
with app.app_context():
    db.create_all()

# API Endpoints
@app.route('/papers', methods=['POST'])
def add_paper():
    """ Add a new research paper."""
    data = request.json
    # Validate required fields
    if not data.get('article_title') or not data.get('authors'):
        return jsonify({"error": "article_title and authors are required fields"}), 400

    try:
        new_paper = ResearchPaper(
            article_title=data['article_title'],
            authors=data['authors'],
            contact_info=data.get('contact_info'),
            year_published=data.get('year_published'),
            institution=data.get('institution'),
            num_publications_used=data.get('num_publications_used'),
            full_link=data.get('full_link'),
            shortened_link=data.get('shortened_link'),
            is_duplicate=data.get('is_duplicate', False),
            qual_score_method=data.get('qual_score_method'),
            study_type=data.get('study_type'),
            qualsyst_criteria=data.get('qualsyst_criteria'),
        )
        db.session.add(new_paper)
        db.session.commit()
        return jsonify({"message": "Paper added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/papers', methods=['GET'])
def get_papers():
    """ Retrieve all research papers."""
    try:
        papers = ResearchPaper.query.all()
        result = [
            {
                "id": paper.id,
                "article_title": paper.article_title,
                "authors": paper.authors,
                "contact_info": paper.contact_info,
                "year_published": paper.year_published,
                "institution": paper.institution,
                "num_publications_used": paper.num_publications_used,
                "full_link": paper.full_link,
                "shortened_link": paper.shortened_link,
                "is_duplicate": paper.is_duplicate,
                "qual_score_method": paper.qual_score_method,
                "study_type": paper.study_type,
                "qualsyst_criteria": paper.qualsyst_criteria,
            }
            for paper in papers
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/papers', methods=['GET'])
def get_paper_by_title():
    title = request.args.get('title')
    if not title:
        return jsonify([]), 200
    papers = ResearchPaper.query.filter(ResearchPaper.article_title.ilike(f"%{title}%")).all()
    result = [
        {"id": paper.id, "article_title": paper.article_title} for paper in papers
    ]
    return jsonify(result), 200



if __name__ == '__main__':
    # Set the host and port
    host = '127.0.0.1'  # Localhost
    port = 5000         # Default Flask port

    # Print the API URL
    print(f"API is running at: http://{host}:{port}")

    # Run the Flask app
    app.run(debug=True, host=host, port=port)
