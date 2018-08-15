# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import random
import jinja2
import os

from google.appengine.api import users

jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
#        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('WAKANDA HAS BEEN HACKED')
        user = users.get_current_user()
        if user is not None:
           self.response.write('Hello Notes:')
           logout_url = users.create_logout_url(self.request.url)
           template_context = {
                   'user': user.nickname(),
                   'logout_url': logout_url,
                   }
           template = jinja_env.get_template('main.html')
           self.response.out.write( 
           template.render(template_context))
        else:
            login_url = users.create_login_url(self.request.uri)
            self.redirect(login_url)
    def post(self):
        user = users.get_current_user()
        if user is None: 
            self.error(401)
        logout_url = users.create_logout_url(self.request.url)
        template_context = {
                'user': user.nickname(),
                'logout_url': logout_url,
                'note_title': self.request.get('title'),
                'note_content': self.request.get('content'),
                }
        template = jinja_env.get_template('main.html')
        self.response.out.write(
                template.render(template_context))

class EmotionHandler(webapp2.RequestHandler):
    def get(self): #responds to a GET request
        a_template = jinja_env.get_template('templates/sample_page.html')
        emotions = ["Happy", "sad", "hangry", "excited"] 
        self.response.out.write(a_template.render(the_variables))

class FoodHandler(webapp2.RequestHandler):
    def get(self): #responds to a GET request
        food = ["Fish", "Tacos", "Chicken", "Pozole", "Birria", "Menudo"]
        self.response.write("today we are having " + random.choice(food))

app = webapp2.WSGIApplication([ 
    ('/', MainPage),
    ('/feelings', EmotionHandler),
    ('/food', FoodHandler),
], debug=True)

#class EmotionHandler(webapp2.RequestHandler):
#   def get(self): #for a get request
#    a_template =  the_jinja_env.get_template('templates.html')
#   the variables = {"an emotion": "happy", "a_day_of_week": "monday"}
#   self.response.out.write a_template.render(the_variables)
