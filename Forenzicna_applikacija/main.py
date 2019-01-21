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


class hairColor:
    black = "CCAGCAATCGC"
    brown = "GCCAGTGCCG"
    blonde = "TTAGCTATCGC"

class facialShape:
    square = "GCCACGG"
    round = "ACCACAA"
    oval = "AGGCCTCA"

class eyeColor:
    blue = "TTGTGGTGGC"
    green = "GGGAGGTGGC"
    brown = "AAGTAGTGAC"

class gender:
    female = "TGAAGGACCTTC"
    male = "TGCAGGAACTTC"

class race:
    white = "AAAACCTCA"
    black = "CGACTACAG"
    asian = "CGCGGGCCG"

eva = {
    "gener": gender.female,
    "race": race.white,
    "hair": hairColor.blonde,
    "eye": eyeColor.blue,
    "face": facialShape.oval
}

larisa = {
    "gener": gender.female,
    "race": race.white,
    "hair": hairColor.brown,
    "eye": eyeColor.brown,
    "face": facialShape.oval
}

matej = {
    "gener": gender.male,
    "race": race.white,
    "hair": hairColor.black,
    "eye": eyeColor.blue,
    "face": facialShape.square
}

miha = {
    "gener": gender.male,
    "race": race.white,
    "hair": hairColor.brown,
    "eye": eyeColor.green,
    "face": facialShape.square
}


suspects = {
    "Eva": eva,
    "Larisa": larisa,
    "Matej": matej,
    "Miha": miha
}


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

    def post(self):
        dna = self.request.get("dna")

        for name, name_list in suspects.iteritems():  # gre čez vsa imena in izpostavi vrednosti (vrednost slovarja)
            perpetrator = ""  # pripravi prazni variable za storilca
            for car, val in name_list.iteritems():  # gre čez vse car - karakteristike oz. čez slovar v slovarju
                if val in dna:  # če se ujema zapiše ime v variable
                    print car + " (" + val + ")" + " = match"
                    perpetrator = name
                else:
                    print car + " (" + val + ")" + " = NO match"
                    perpetrator = ""  # če se ne ujema resetira variable
                    break  # Zelo pomemben breake!!! Če tu ni breake, vrne za storilca Mateja, ker ima zadnji parameter, ki se ujema z DNA in zato vpiše ime v varable. S tem breakeom nehamo testirati ob prvem neskladju!
            if perpetrator:  # če se ujemajo vsi pogoji ima ima ergo ni prazen zato zaključi iskanje
                print "\nPrekini test. Storilec je znan! Vsi DNA parametri se ujemajo!"
                # perpetrator != ""
                break
            else:
                perpetrator = "neznan"
        if perpetrator == "neznan":
            message = "<div style='color: red;'>Storilec je " + perpetrator + "</div>"
        else:
            message = "<div style='color: green;'>Storilec je " + perpetrator + "</div>"

        params = {"message": message}

        return self.render_template("odgovor.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)