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

class Blogs(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

class BlogFront(Handler):
    def render_front(self, title="", content="", error=""):
        posts = db.GqlQuery("SELECT * FROM Blogs ORDER BY created DESC LIMIT 5")

        self.render("frontpage.html", title=title, content=content, error=error, posts=posts )

    def get(self):
        self.render_front()

class NewPost(Handler):
    def get(self):
        self.render("add-post.html")

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        if title and content:
            p = Blogs(title = title, content = content)
            p.put()
            self.redirect("/blog")
        else:
            error = "you need both a title and blog content!"
            self.render_front(title, content, error)


app = webapp2.WSGIApplication([
    #('/', MainPage),
    ('/blog', BlogFront),
    ('/newpost', NewPost)
], debug=True)
