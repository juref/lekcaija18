#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import random
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


country_capital_dict = {"Slovenija": "Ljubljana", "Hrvaska": "Zagreb", "Avstrija": "Dunaj", "Italija": "Rim"}




class MainHandler(BaseHandler):
    def get(self):
        random_num = random.randint(0, 3)
        drzava = country_capital_dict.keys()[random_num]
        mesto = country_capital_dict.get(drzava)

        drzava_in = {"drzava": drzava, "mesto": mesto}

        return self.render_template("index.html", params=drzava_in)

    def post(self):
        secret =self.request.get("mesto")
        guess = self.request.get("guess")

        if secret.lower() == guess.lower():
            message = "<b>Bravo! Odgovor je pravilen!</b>"
            class_from_main = "right"
        else:
            message = "Narobe, " + str(guess.title()) + " ni pravilen odgvor.</p>"
            class_from_main = "wrong"

        params = {"message": message,
                  "class_from_main": class_from_main,
                  }

        return self.render_template("odgovor.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)