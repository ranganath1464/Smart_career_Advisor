# matcher/learning_path.py

def get_learning_resources(skill_gap):
    # Mapping each skill to a learning resource (can be improved later)
    resource_links = {
        "python": "https://www.learnpython.org/",
        "sql": "https://www.codecademy.com/learn/learn-sql",
        "excel": "https://www.microsoft.com/en-us/microsoft-365/excel",
        "tableau": "https://www.coursera.org/learn/tableau",
        "power bi": "https://learn.microsoft.com/en-us/power-bi/",
        "numpy": "https://numpy.org/learn/",
        "pandas": "https://pandas.pydata.org/docs/",
        "scikit-learn": "https://scikit-learn.org/stable/tutorial/index.html",
        "tensorflow": "https://www.tensorflow.org/tutorials",
        "keras": "https://keras.io/getting_started/",
        "flask": "https://flask.palletsprojects.com/en/2.3.x/tutorial/",
        "django": "https://docs.djangoproject.com/en/4.2/intro/",
        "nlp": "https://www.coursera.org/specializations/natural-language-processing",
        "machine learning": "https://www.coursera.org/learn/machine-learning",
        "deep learning": "https://www.coursera.org/specializations/deep-learning",
        "data visualization": "https://www.coursera.org/learn/dataviz",
        "matplotlib": "https://matplotlib.org/stable/tutorials/index.html",
        "seaborn": "https://seaborn.pydata.org/tutorial.html",
        "api": "https://www.restapitutorial.com/",
        "git": "https://www.atlassian.com/git/tutorials",
        "linux": "https://linuxjourney.com/"
    }

    learning_path = {}
    for skill in skill_gap:
        if skill.lower() in resource_links:
            learning_path[skill] = resource_links[skill.lower()]

    return learning_path
