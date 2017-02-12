import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class BlogFront(Handler):
    def render_front(self, subject="", content="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        self.render("frontpage.html", subject=subject, content=content, error=error, posts=posts )

    def get(self):
         self.render_front()

class NewPost(Handler):
    def render_new(self, subject="", content="", error=""):
        self.render("new-post.html", subject=subject, content=content, error=error)

    def get(self):
         self.render_new()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            a = Post(subject = subject, content = content)
            a.put()

            self.redirect("/blog")
        else:
            error = "we need both a subject and some content!"
            self.render_new(subject, content, error)

app = webapp2.WSGIApplication([
    ('/', BlogFront),
    ('/blog', BlogFront),
    ('/newpost', NewPost)
], debug=True)
