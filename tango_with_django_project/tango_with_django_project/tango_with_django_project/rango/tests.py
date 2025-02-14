#
# Tango with Django 2 Progress Tests
# By Leif Azzopardi and David Maxwell
# With assistance from Enzo Roiz (https://github.com/enzoroiz)
#
# Chapter 3 -- Django Basics
# Last updated October 3rd, 2019
# Revising Author: David Maxwell
#

#
# In order to run these tests, copy this module to your tango_with_django_project/rango/ directory.
# Once this is complete, run $ python manage.py test rango.tests_chapter3
#
# The tests will then be run, and the output displayed -- do you pass them all?
#
# Once you are done with the tests, delete the module. You don't need to put it in your Git repository!
#

import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class Chapter3ProjectStructureTests(TestCase):
    """
    Simple tests to probe the file structure of your project so far.
    We also include a test to check whether you have added rango to your list of INSTALLED_APPS.
    """

    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.rango_app_dir = os.path.join(self.project_base_dir, 'rango')

    def test_project_created(self):
        """
        Tests whether the tango_with_django_project configuration directory is present and correct.
        """
        directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'tango_with_django_project'))
        urls_module_exists = os.path.isfile(os.path.join(self.project_base_dir, 'tango_with_django_project', 'urls.py'))

        self.assertTrue(directory_exists,
                        f"{FAILURE_HEADER}Your tango_with_django_project configuration directory doesn't seem to exist. Did you use the correct name?{FAILURE_FOOTER}")
        self.assertTrue(urls_module_exists,
                        f"{FAILURE_HEADER}Your project's urls.py module does not exist. Did you use the startproject command?{FAILURE_FOOTER}")

    def test_rango_app_created(self):
        """
        Determines whether the Rango app has been created.
        """
        directory_exists = os.path.isdir(self.rango_app_dir)
        is_python_package = os.path.isfile(os.path.join(self.rango_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(os.path.join(self.rango_app_dir, 'views.py'))

        self.assertTrue(directory_exists,
                        f"{FAILURE_HEADER}The rango app directory does not exist. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(is_python_package,
                        f"{FAILURE_HEADER}The rango directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(views_module_exists,
                        f"{FAILURE_HEADER}The rango directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")

    def test_rango_has_urls_module(self):
        """
        Did you create a separate urls.py module for Rango?
        """
        module_exists = os.path.isfile(os.path.join(self.rango_app_dir, 'urls.py'))
        self.assertTrue(module_exists,
                        f"{FAILURE_HEADER}The rango app's urls.py module is missing. Read over the instructions carefully, and try again. You need TWO urls.py modules.{FAILURE_FOOTER}")

    def test_is_rango_app_configured(self):
        """
        Did you add the new Rango app to your INSTALLED_APPS list?
        """
        is_app_configured = 'rango' in settings.INSTALLED_APPS

        self.assertTrue(is_app_configured,
                        f"{FAILURE_HEADER}The rango app is missing from your setting's INSTALLED_APPS list.{FAILURE_FOOTER}")


class Chapter3IndexPageTests(TestCase):
    """
    Testing the basics of your index view and URL mapping.
    Also runs tests to check the response from the server.
    """

    def setUp(self):
        self.views_module = importlib.import_module('rango.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('tango_with_django_project.urls')

    def test_view_exists(self):
        """
        Does the index() view exist in Rango's views.py module?
        """
        name_exists = 'index' in self.views_module_listing
        is_callable = callable(self.views_module.index)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The index() view for rango does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable,
                        f"{FAILURE_HEADER}Check that you have created the index() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in Rango's urls.py.
        We have the 'index' view named twice -- it should resolve to '/rango/'.
        """
        index_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'index':
                    index_mapping_exists = True

        self.assertTrue(index_mapping_exists,
                        f"{FAILURE_HEADER}The index URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('rango:index'), '/rango/',
                          f"{FAILURE_HEADER}The index URL lookup failed. Check Rango's urls.py module. You're missing something in there.{FAILURE_FOOTER}")

    def test_response(self):
        """
        Does the response from the server contain the required string?
        """
        response = self.client.get(reverse('rango:index'))

        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}Requesting the index page failed. Check your URLs and view.{FAILURE_FOOTER}")
        self.assertContains(response, "Rango says hey there partner!",
                            msg_prefix=f"{FAILURE_HEADER}The index view does not return the expected response. Be careful you haven't missed any punctuation, and that your cAsEs are correct.{FAILURE_FOOTER}")

    def test_for_about_hyperlink(self):
        """
        Does the response contain the about hyperlink required in the exercise?
        Checks for both single and double quotes in the attribute. Both are acceptable.
        """
        response = self.client.get(reverse('rango:index'))

        single_quotes_check = '<a href=\'/rango/about/\'>About</a>' in response.content.decode() or '<a href=\'/rango/about\'>About</a>' in response.content.decode()
        double_quotes_check = '<a href="/rango/about/">About</a>' in response.content.decode() or '<a href="/rango/about">About</a>' in response.content.decode()

        self.assertTrue(single_quotes_check or double_quotes_check,
                        f"{FAILURE_HEADER}We couldn't find the hyperlink to the /rango/about/ URL in your index page. Check that it appears EXACTLY as in the book.{FAILURE_FOOTER}")


class Chapter3AboutPageTests(TestCase):
    """
    Tests to check the about view.
    We check whether the view exists, the mapping is correct, and the response is correct.
    """

    def setUp(self):
        self.views_module = importlib.import_module('rango.views')
        self.views_module_listing = dir(self.views_module)

    def test_view_exists(self):
        """
        Does the about() view exist in Rango's views.py module?
        """
        name_exists = 'about' in self.views_module_listing
        is_callable = callable(self.views_module.about)

        self.assertTrue(name_exists,
                        f"{FAILURE_HEADER}We couldn't find the view for your about view! It should be called about().{FAILURE_FOOTER}")
        self.assertTrue(is_callable,
                        f"{FAILURE_HEADER}Check you have defined your about() view correctly. We can't execute it.{FAILURE_FOOTER}")

    def test_mapping_exists(self):
        """
        Checks whether the about view has the correct URL mapping.
        """
        self.assertEquals(reverse('rango:about'), '/rango/about/',
                          f"{FAILURE_HEADER}Your about URL mapping is either missing or mistyped.{FAILURE_FOOTER}")

    def test_response(self):
        """
        Checks whether the view returns the required string to the client.
        """
        response = self.client.get(reverse('rango:about'))

        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}When requesting the about view, the server did not respond correctly. Is everything correct in your URL mappings and the view?{FAILURE_FOOTER}")
        self.assertContains(response, "Rango says here is the about page.",
                            msg_prefix=f"{FAILURE_HEADER}The about view did not respond with the expected message. Check that the message matches EXACTLY with what is requested of you in the book.{FAILURE_FOOTER}")

    def test_for_index_hyperlink(self):
        """
        Does the response contain the index hyperlink required in the exercise?
        Checks for both single and double quotes in the attribute. Both are acceptable.
        """
        response = self.client.get(reverse('rango:about'))

        single_quotes_check = '<a href=\'/rango/\'>Index</a>' in response.content.decode()
        double_quotes_check = '<a href="/rango/">Index</a>' in response.content.decode()

        self.assertTrue(single_quotes_check or double_quotes_check,
                        f"{FAILURE_HEADER}We could not find a hyperlink back to the index page in your about view. Check your about.html template, and try again.{FAILURE_FOOTER}")


#
# Tango with Django 2 Progress Tests
# By Leif Azzopardi and David Maxwell
# With assistance from Enzo Roiz (https://github.com/enzoroiz)
#
# Chapter 4 -- Templates and Media Files
# Last updated January 25th, 2020
# Revising Author: David Maxwell
#

#
# In order to run these tests, copy this module to your tango_with_django_project/rango/ directory.
# Once this is complete, run $ python manage.py test rango.tests_chapter4
#
# The tests will then be run, and the output displayed -- do you pass them all?
#
# Once you are done with the tests, delete the module. You don't need to put it in your Git repository!
#

import os
import re
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class Chapter4TemplatesStructureTests(TestCase):
    """
    Have you set templates, static files and media files up correctly, as per the book?
    """

    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.rango_templates_dir = os.path.join(self.templates_dir, 'rango')

    def test_templates_directory_exists(self):
        """
        Does the templates/ directory exist?
        """
        directory_exists = os.path.isdir(self.templates_dir)
        self.assertTrue(directory_exists,
                        f"{FAILURE_HEADER}Your project's templates directory does not exist.{FAILURE_FOOTER}")

    def test_rango_templates_directory_exists(self):
        """
        Does the templates/rango/ directory exist?
        """
        directory_exists = os.path.isdir(self.rango_templates_dir)
        self.assertTrue(directory_exists,
                        f"{FAILURE_HEADER}The Rango templates directory does not exist.{FAILURE_FOOTER}")

    def test_template_dir_setting(self):
        """
        Does the TEMPLATE_DIR setting exist, and does it point to the right directory?
        """
        variable_exists = 'TEMPLATE_DIR' in dir(settings)
        self.assertTrue(variable_exists,
                        f"{FAILURE_HEADER}Your settings.py module does not have the variable TEMPLATE_DIR defined!{FAILURE_FOOTER}")

        template_dir_value = os.path.normpath(settings.TEMPLATE_DIR)
        template_dir_computed = os.path.normpath(self.templates_dir)
        self.assertEqual(template_dir_value, template_dir_computed,
                         f"{FAILURE_HEADER}Your TEMPLATE_DIR setting does not point to the expected path. Check your configuration, and try again.{FAILURE_FOOTER}")

    def test_template_lookup_path(self):
        """
        Does the TEMPLATE_DIR value appear within the lookup paths for templates?
        """
        lookup_list = settings.TEMPLATES[0]['DIRS']
        found_path = False

        for entry in lookup_list:
            entry_normalised = os.path.normpath(entry)

            if entry_normalised == os.path.normpath(settings.TEMPLATE_DIR):
                found_path = True

        self.assertTrue(found_path,
                        f"{FAILURE_HEADER}Your project's templates directory is not listed in the TEMPLATES>DIRS lookup list. Check your settings.py module.{FAILURE_FOOTER}")

    def test_templates_exist(self):
        """
        Do the index.html and about.html templates exist in the correct place?
        """
        index_path = os.path.join(self.rango_templates_dir, 'index.html')
        about_path = os.path.join(self.rango_templates_dir, 'about.html')

        self.assertTrue(os.path.isfile(index_path),
                        f"{FAILURE_HEADER}Your index.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(about_path),
                        f"{FAILURE_HEADER}Your about.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")


class Chapter4IndexPageTests(TestCase):
    """
    A series of tests to ensure that the index page/view has been updated to work with templates.
    Image tests are in the Chapter4StaticMediaTests suite.
    """

    def setUp(self):
        self.response = self.client.get(reverse('rango:index'))

    def test_index_uses_template(self):
        """
        Checks whether the index view uses a template -- and the correct one!
        """
        self.assertTemplateUsed(self.response, 'rango/index.html',
                                f"{FAILURE_HEADER}Your index() view does not use the expected index.html template.{FAILURE_FOOTER}")

    def test_index_uses_context_dictionary(self):
        """
        Tests whether the index view uses the context dictionary correctly.
        Crunchy, creamy cookie, anyone?
        """
        self.assertTrue('boldmessage' in self.response.context,
                        f"{FAILURE_HEADER}In your index view, the context dictionary is not passing the boldmessage key. Check your context dictionary in the index() view, located in rango/views.py, and try again.{FAILURE_FOOTER}")

        message = self.response.context['boldmessage']
        expected = 'Crunchy, creamy, cookie, candy, cupcake!'
        self.assertEqual(message, expected,
                         f"{FAILURE_HEADER}The boldmessage being sent to the index.html template does not match what is expected. Check your index() view. Make sure you match up cases, and don't miss any punctuation! Even one missing character will cause the test to fail.{FAILURE_FOOTER}")

    def test_index_starts_with_doctype(self):
        """
        Is the <!DOCTYPE html> declaration on the first line of the index.html template?
        """
        self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'),
                        f"{FAILURE_HEADER}Your index.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FAILURE_FOOTER}")

    def test_about_link_present(self):
        """
        Is the about hyperlink present and correct on the index.html template?
        """
        expected = "<a href=\"/rango/about/\">About</a><br />"
        self.assertTrue(expected in self.response.content.decode(),
                        f"{FAILURE_HEADER}Your index.html template doesn't contain the /rango/about/ link -- or it is not correct. Make sure you have the linebreak in, too!{FAILURE_FOOTER}")


class Chapter4StaticMediaTests(TestCase):
    """
    A series of tests to check whether static files and media files have been setup and used correctly.
    Also tests for the two required files -- rango.jpg and cat.jpg.
    """

    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.static_dir = os.path.join(self.project_base_dir, 'static')
        self.media_dir = os.path.join(self.project_base_dir, 'media')

    def test_does_static_directory_exist(self):
        """
        Tests whether the static directory exists in the correct location -- and the images subdirectory.
        Also checks for the presence of rango.jpg in the images subdirectory.
        """
        does_static_dir_exist = os.path.isdir(self.static_dir)
        does_images_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'images'))
        does_rango_jpg_exist = os.path.isfile(os.path.join(self.static_dir, 'images', 'rango.jpg'))

        self.assertTrue(does_static_dir_exist,
                        f"{FAILURE_HEADER}The static directory was not found in the expected location. Check the instructions in the book, and try again.{FAILURE_FOOTER}")
        self.assertTrue(does_images_static_dir_exist,
                        f"{FAILURE_HEADER}The images subdirectory was not found in your static directory.{FAILURE_FOOTER}")
        self.assertTrue(does_rango_jpg_exist,
                        f"{FAILURE_HEADER}We couldn't locate the rango.jpg image in the /static/images/ directory. If you think you've included the file, make sure to check the file extension. Sometimes, a JPG can have the extension .jpeg. Be careful! It must be .jpg for this test.{FAILURE_FOOTER}")

    def test_does_media_directory_exist(self):
        """
        Tests whether the media directory exists in the correct location.
        Also checks for the presence of cat.jpg.
        """
        does_media_dir_exist = os.path.isdir(self.media_dir)
        does_cat_jpg_exist = os.path.isfile(os.path.join(self.media_dir, 'cat.jpg'))

        self.assertTrue(does_media_dir_exist,
                        f"{FAILURE_HEADER}We couldn't find the /media/ directory in the expected location. Make sure it is in your project directory (at the same level as the manage.py module).{FAILURE_FOOTER}")
        self.assertTrue(does_cat_jpg_exist,
                        f"{FAILURE_HEADER}We couldn't find the cat.jpg image in /media/. Check the file extension; this is a common pitfall. It should .jpg. Not .png, .gif, or .jpeg!{FAILURE_FOOTER}")

    def test_static_and_media_configuration(self):
        """
        Performs a number of tests on your Django project's settings in relation to static files and user upload-able files..
        """
        static_dir_exists = 'STATIC_DIR' in dir(settings)
        self.assertTrue(static_dir_exists,
                        f"{FAILURE_HEADER}Your settings.py module does not have the variable STATIC_DIR defined.{FAILURE_FOOTER}")

        expected_path = os.path.normpath(self.static_dir)
        static_path = os.path.normpath(settings.STATIC_DIR)
        self.assertEqual(expected_path, static_path,
                         f"{FAILURE_HEADER}The value of STATIC_DIR does not equal the expected path. It should point to your project root, with 'static' appended to the end of that.{FAILURE_FOOTER}")

        staticfiles_dirs_exists = 'STATICFILES_DIRS' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists,
                        f"{FAILURE_HEADER}The required setting STATICFILES_DIRS is not present in your project's settings.py module. Check your settings carefully. So many students have mistyped this one.{FAILURE_FOOTER}")
        self.assertEqual([static_path], settings.STATICFILES_DIRS,
                         f"{FAILURE_HEADER}Your STATICFILES_DIRS setting does not match what is expected. Check your implementation against the instructions provided.{FAILURE_FOOTER}")

        staticfiles_dirs_exists = 'STATIC_URL' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists,
                        f"{FAILURE_HEADER}The STATIC_URL variable has not been defined in settings.py.{FAILURE_FOOTER}")
        self.assertEqual('/static/', settings.STATIC_URL,
                         f"{FAILURE_HEADER}STATIC_URL does not meet the expected value of /static/. Make sure you have a slash at the end!{FAILURE_FOOTER}")

        media_dir_exists = 'MEDIA_DIR' in dir(settings)
        self.assertTrue(media_dir_exists,
                        f"{FAILURE_HEADER}The MEDIA_DIR variable in settings.py has not been defined.{FAILURE_FOOTER}")

        expected_path = os.path.normpath(self.media_dir)
        media_path = os.path.normpath(settings.MEDIA_DIR)
        self.assertEqual(expected_path, media_path,
                         f"{FAILURE_HEADER}The MEDIA_DIR setting does not point to the correct path. Remember, it should have an absolute reference to tango_with_django_project/media/.{FAILURE_FOOTER}")

        media_root_exists = 'MEDIA_ROOT' in dir(settings)
        self.assertTrue(media_root_exists,
                        f"{FAILURE_HEADER}The MEDIA_ROOT setting has not been defined.{FAILURE_FOOTER}")

        media_root_path = os.path.normpath(settings.MEDIA_ROOT)
        self.assertEqual(media_path, media_root_path,
                         f"{FAILURE_HEADER}The value of MEDIA_ROOT does not equal the value of MEDIA_DIR.{FAILURE_FOOTER}")

        media_url_exists = 'MEDIA_URL' in dir(settings)
        self.assertTrue(media_url_exists,
                        f"{FAILURE_HEADER}The setting MEDIA_URL has not been defined in settings.py.{FAILURE_FOOTER}")

        media_url_value = settings.MEDIA_URL
        self.assertEqual('/media/', media_url_value,
                         f"{FAILURE_HEADER}Your value of the MEDIA_URL setting does not equal /media/. Check your settings!{FAILURE_FOOTER}")

    def test_context_processor_addition(self):
        """
        Checks to see whether the media context_processor has been added to your project's settings module.
        """
        context_processors_list = settings.TEMPLATES[0]['OPTIONS']['context_processors']
        self.assertTrue('django.template.context_processors.media' in context_processors_list,
                        f"{FAILURE_HEADER}The 'django.template.context_processors.media' context processor was not included. Check your settings.py module.{FAILURE_FOOTER}")


class Chapter4ExerciseTests(TestCase):
    """
    A series of tests to ensure that the exercise listing at the end of Chapter 4 has been completed.
    """

    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.template_dir = os.path.join(self.project_base_dir, 'templates', 'rango')
        self.about_response = self.client.get(reverse('rango:about'))

    def test_about_template_exists(self):
        """
        Tests the about template -- if it exists, and whether or not the about() view makes use of it.
        """
        template_exists = os.path.isfile(os.path.join(self.template_dir, 'about.html'))
        self.assertTrue(template_exists,
                        f"{FAILURE_HEADER}The about.html template was not found in the expected location.{FAILURE_FOOTER}")

    def test_about_uses_template(self):
        """
        Checks whether the index view uses a template -- and the correct one!
        """
        self.assertTemplateUsed(self.about_response, 'rango/about.html',
                                f"{FAILURE_HEADER}The about() view does not use the about.html template.{FAILURE_FOOTER}")

    def test_about_starts_with_doctype(self):
        """
        Is the <!DOCTYPE html> declaration on the first line of the about.html template?
        """
        self.assertTrue(self.about_response.content.decode().startswith('<!DOCTYPE html>'),
                        f"{FAILURE_HEADER}Your about.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FAILURE_FOOTER}")

    def test_about_contains_required_text(self):
        """
        Checks to see whether the required text is on the rendered about page.
        """
        required = [
            "here is the about page.",
            "This tutorial has been put together by "
        ]

        for required_str in required:
            self.assertTrue(required_str in self.about_response.content.decode(),
                            f"{FAILURE_HEADER}The expected string '{required_str}' was not found in the rendered /rango/about/ response.{FAILURE_FOOTER}")

    def test_about_contains_rango(self):
        """
        Checks whether the rendered about view has the picture of Rango.
        """
        required_str = f"<img src=\"{settings.STATIC_URL}images/rango.jpg\" alt=\"Picture of Rango\" />"
        self.assertTrue(required_str in self.about_response.content.decode(),
                        f"{FAILURE_HEADER}The HTML markup to include the image of Rango in the about template was not found. It needs to match exactly what we are looking for. Check the book.{FAILURE_FOOTER}")

    def test_about_contains_cat(self):
        """
        Checks whether the rendered about view has the picture of a cat.
        We need to be a little bit lenient here as the example above includes a period, and in the exercise instructions, the required alt text is ended with a period. Either with or without is acceptable.
        """
        required_pattern = f"<img src=\"{settings.MEDIA_URL}cat.jpg\" alt=\"Picture of a Cat.?\" />"
        self.assertTrue(re.search(required_pattern, self.about_response.content.decode()),
                        f"{FAILURE_HEADER}The HTML markup to include the image of a cat in the about template was not found. It needs to match exactly what we are looking for. Check the book.{FAILURE_FOOTER}")


#
# Tango with Django 2 Progress Tests
# By Leif Azzopardi and David Maxwell
# With assistance from Enzo Roiz (https://github.com/enzoroiz)
#
# Chapter 5 -- Models and Databases
# Last updated: October 3rd, 2019
# Revising Author: David Maxwell
#

#
# In order to run these tests, copy this module to your tango_with_django_project/rango/ directory.
# Once this is complete, run $ python manage.py test rango.tests_chapter5
#
# The tests will then be run, and the output displayed -- do you pass them all?
#
# Once you are done with the tests, delete the module. You don't need to put it in your Git repository!
#

import os
import warnings
import importlib
from rango.models import Category, Page
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class Chapter5DatabaseConfigurationTests(TestCase):
    """
    Is your database configured as the book states?
    These tests should pass if you haven't tinkered with the database configuration.
    N.B. Some of the configuration values we could check are overridden by the testing framework -- so we leave them.
    """

    def setUp(self):
        pass

    def does_gitignore_include_database(self, path):
        """
        Takes the path to a .gitignore file, and checks to see whether the db.sqlite3 database is present in that file.
        """
        f = open(path, 'r')

        for line in f:
            line = line.strip()

            if line.startswith('db.sqlite3'):
                return True

        f.close()
        return False

    def test_databases_variable_exists(self):
        """
        Does the DATABASES settings variable exist, and does it have a default configuration?
        """
        self.assertTrue(settings.DATABASES,
                        f"{FAILURE_HEADER}Your project's settings module does not have a DATABASES variable, which is required. Check the start of Chapter 5.{FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES,
                        f"{FAILURE_HEADER}You do not have a 'default' database configuration in your project's DATABASES configuration variable. Check the start of Chapter 5.{FAILURE_FOOTER}")

    def test_gitignore_for_database(self):
        """
        If you are using a Git repository and have set up a .gitignore, checks to see whether the database is present in that file.
        """
        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()

        if git_base_dir.startswith('fatal'):
            warnings.warn(
                "You don't appear to be using a Git repository for your codebase. Although not strictly required, it's *highly recommended*. Skipping this test.")
        else:
            gitignore_path = os.path.join(git_base_dir, '.gitignore')

            if os.path.exists(gitignore_path):
                self.assertTrue(self.does_gitignore_include_database(gitignore_path),
                                f"{FAILURE_HEADER}Your .gitignore file does not include 'db.sqlite3' -- you should exclude the database binary file from all commits to your Git repository.{FAILURE_FOOTER}")
            else:
                warnings.warn(
                    "You don't appear to have a .gitignore file in place in your repository. We ask that you consider this! Read the Don't git push your Database paragraph in Chapter 5.")


class Chapter5ModelTests(TestCase):
    """
    Are the models set up correctly, and do all the required attributes (post exercises) exist?
    """

    def setUp(self):
        category_py = Category.objects.get_or_create(name='Python', views=123, likes=55)
        Category.objects.get_or_create(name='Django', views=187, likes=90)

        Page.objects.get_or_create(category=category_py[0],
                                   title='Tango with Django',
                                   url='https://www.tangowithdjango.com',
                                   views=156)

    def test_category_model(self):
        """
        Runs a series of tests on the Category model.
        Do the correct attributes exist?
        """
        category_py = Category.objects.get(name='Python')
        self.assertEqual(category_py.views, 123,
                         f"{FAILURE_HEADER}Tests on the Category model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(category_py.likes, 55,
                         f"{FAILURE_HEADER}Tests on the Category model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")

        category_dj = Category.objects.get(name='Django')
        self.assertEqual(category_dj.views, 187,
                         f"{FAILURE_HEADER}Tests on the Category model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(category_dj.likes, 90,
                         f"{FAILURE_HEADER}Tests on the Category model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")

    def test_page_model(self):
        """
        Runs some tests on the Page model.
        Do the correct attributes exist?
        """
        category_py = Category.objects.get(name='Python')
        page = Page.objects.get(title='Tango with Django')
        self.assertEqual(page.url, 'https://www.tangowithdjango.com',
                         f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(page.views, 156,
                         f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(page.title, 'Tango with Django',
                         f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(page.category, category_py,
                         f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")

    def test_str_method(self):
        """
        Tests to see if the correct __str__() method has been implemented for each model.
        """
        category_py = Category.objects.get(name='Python')
        page = Page.objects.get(title='Tango with Django')

        self.assertEqual(str(category_py), 'Python',
                         f"{FAILURE_HEADER}The __str__() method in the Category class has not been implemented according to the specification given in the book.{FAILURE_FOOTER}")
        self.assertEqual(str(page), 'Tango with Django',
                         f"{FAILURE_HEADER}The __str__() method in the Page class has not been implemented according to the specification given in the book.{FAILURE_FOOTER}")


class Chapter5AdminInterfaceTests(TestCase):
    """
    A series of tests that examines the authentication functionality (for superuser creation and logging in), and admin interface changes.
    Have all the admin interface tweaks been applied, and have the two models been added to the admin app?
    """

    def setUp(self):
        """
        Create a superuser account for use in testing.
        Logs the superuser in, too!
        """
        User.objects.create_superuser('testAdmin', 'email@email.com', 'adminPassword123')
        self.client.login(username='testAdmin', password='adminPassword123')

        category = Category.objects.get_or_create(name='TestCategory')[0]
        Page.objects.get_or_create(title='TestPage1', url='https://www.google.com', category=category)

    def test_admin_interface_accessible(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}The admin interface is not accessible. Check that you didn't delete the 'admin/' URL pattern in your project's urls.py module.{FAILURE_FOOTER}")

    def test_models_present(self):
        """
        Checks whether the two models are present within the admin interface homepage -- and whether Rango is listed there at all.
        """
        response = self.client.get('/admin/')
        response_body = response.content.decode()

        # Is the Rango app present in the admin interface's homepage?
        self.assertTrue('Models in the Rango application' in response_body,
                        f"{FAILURE_HEADER}The Rango app wasn't listed on the admin interface's homepage. You haven't added the models to the admin interface.{FAILURE_FOOTER}")

        # Check each model is present.
        self.assertTrue('Categories' in response_body,
                        f"{FAILURE_HEADER}The Category model was not found in the admin interface. If you did add the model to admin.py, did you add the correct plural spelling (Categories)?{FAILURE_FOOTER}")
        self.assertTrue('Pages' in response_body,
                        f"{FAILURE_HEADER}The Page model was not found in the admin interface. If you did add the model to admin.py, did you add the correct plural spelling (Pages)?{FAILURE_FOOTER}")

    def test_page_display_changes(self):
        """
        Checks to see whether the Page model has had the required changes applied for presentation in the admin interface.
        """
        response = self.client.get('/admin/rango/page/')
        response_body = response.content.decode()

        # Headers -- are they all present?
        self.assertTrue('<div class="text"><a href="?o=1">Title</a></div>' in response_body,
                        f"{FAILURE_HEADER}The 'Title' column could not be found in the admin interface for the Page model -- if it is present, is it in the correct order?{FAILURE_FOOTER}")
        self.assertTrue('<div class="text"><a href="?o=2">Category</a></div>' in response_body,
                        f"{FAILURE_HEADER}The 'Category' column could not be found in the admin interface for the Page model -- if it is present, is it in the correct order?{FAILURE_FOOTER}")
        self.assertTrue('<div class="text"><a href="?o=3">Url</a></div>' in response_body,
                        f"{FAILURE_HEADER}The 'Url' (stylised that way!) column could not be found in the admin interface for the Page model -- if it is present, is it in the correct order?{FAILURE_FOOTER}")

        # Is the TestPage1 page present, and in order?
        expected_str = '<tr class="row1"><td class="action-checkbox"><input type="checkbox" name="_selected_action" value="1" class="action-select"></td><th class="field-title"><a href="/admin/rango/page/1/change/">TestPage1</a></th><td class="field-category nowrap">TestCategory</td><td class="field-url">https://www.google.com</td></tr>'
        self.assertTrue(expected_str in response_body,
                        f"{FAILURE_HEADER}We couldn't find the correct output in the Page view within the admin interface for page listings. Did you complete the exercises, adding extra columns to the admin view for this model? Are the columns in the correct order?{FAILURE_FOOTER}")


class Chapter5PopulationScriptTests(TestCase):
    """
    Tests whether the population script puts the expected data into a test database.
    All values that are explicitly mentioned in the book are tested.
    Expects that the population script has the populate() function, as per the book!
    """

    def setUp(self):
        """
        Imports and runs the population script, calling the populate() method.
        """
        try:
            import populate_rango
        except ImportError:
            raise ImportError(
                f"{FAILURE_HEADER}The Chapter 5 tests could not import the populate_rango. Check it's in the right location (the first tango_with_django_project directory).{FAILURE_FOOTER}")

        if 'populate' not in dir(populate_rango):
            raise NameError(
                f"{FAILURE_HEADER}The populate() function does not exist in the populate_rango module. This is required.{FAILURE_FOOTER}")

        # Call the population script -- any exceptions raised here do not have fancy error messages to help readers.
        populate_rango.populate()

    def test_categories(self):
        """
        There should be three categories from populate_rango -- Python, Django and Other Frameworks.
        """
        categories = Category.objects.filter()
        categories_len = len(categories)
        categories_strs = map(str, categories)

        self.assertEqual(categories_len, 3,
                         f"{FAILURE_HEADER}Expecting 3 categories to be created from the populate_rango module; found {categories_len}.{FAILURE_FOOTER}")
        self.assertTrue('Python' in categories_strs,
                        f"{FAILURE_HEADER}The category 'Python' was expected but not created by populate_rango.{FAILURE_FOOTER}")
        self.assertTrue('Django' in categories_strs,
                        f"{FAILURE_HEADER}The category 'Django' was expected but not created by populate_rango.{FAILURE_FOOTER}")
        self.assertTrue('Other Frameworks' in categories_strs,
                        f"{FAILURE_HEADER}The category 'Other Frameworks' was expected but not created by populate_rango.{FAILURE_FOOTER}")

    def test_pages(self):
        """
        Tests to check whether each page for the three different categories exists in the database.
        Calls the helper check_category_pages() method for this.
        """
        details = {'Python':
                       ['Official Python Tutorial', 'How to Think like a Computer Scientist',
                        'Learn Python in 10 Minutes'],
                   'Django':
                       ['Official Django Tutorial', 'Django Rocks', 'How to Tango with Django'],
                   'Other Frameworks':
                       ['Bottle', 'Flask']}

        for category in details:
            page_titles = details[category]
            self.check_category_pages(category, page_titles)

    def test_counts(self):
        """
        Tests whether each category's likes and views values are the values that are stated in the book.
        Pukes when a value doesn't match.
        """
        details = {'Python': {'views': 128, 'likes': 64},
                   'Django': {'views': 64, 'likes': 32},
                   'Other Frameworks': {'views': 32, 'likes': 16}}

        for category in details:
            values = details[category]
            category = Category.objects.get(name=category)
            self.assertEqual(category.views, values['views'],
                             f"{FAILURE_HEADER}The number of views for the '{category}' category is incorrect (got {category.views}, expected {values['views']}, generated from populate_rango).{FAILURE_FOOTER}")
            self.assertEqual(category.likes, values['likes'],
                             f"{FAILURE_HEADER}The number of likes for the '{category}' category is incorrect (got {category.likes}, expected {values['likes']}, generated from populate_rango).{FAILURE_FOOTER}")

    def check_category_pages(self, category, page_titles):
        """
        Performs a number of tests on the database regarding pages for a given category.
        Do all the included pages in the population script exist?
        The expected page list is passed as page_titles. The name of the category is passed as category.
        """
        category = Category.objects.get(name=category)
        pages = Page.objects.filter(category=category)
        pages_len = len(pages)
        page_titles_len = len(page_titles)

        self.assertEqual(pages_len, len(page_titles),
                         f"{FAILURE_HEADER}Expected {page_titles_len} pages in the Python category produced by populate_rango; found {pages_len}.{FAILURE_FOOTER}")

        for title in page_titles:
            try:
                page = Page.objects.get(title=title)
            except Page.DoesNotExist:
                raise ValueError(
                    f"{FAILURE_HEADER}The page '{title}' belonging to category '{category}' was not found in the database produced by populate_rango.{FAILURE_FOOTER}")

            self.assertEqual(page.category, category)

# Tango with Django 2 Progress Tests
# By Leif Azzopardi and David Maxwell
# With assistance from Enzo Roiz (https://github.com/enzoroiz)
#
# Chapter 6 -- Models, Templates and Views
# Last updated: October 15th, 2019
# Revising Author: David Maxwell
#

#
# In order to run these tests, copy this module to your tango_with_django_project/rango/ directory.
# Once this is complete, run $ python manage.py test rango.tests_chapter6
#
# The tests will then be run, and the output displayed -- do you pass them all?
#
# Once you are done with the tests, delete the module. You don't need to put it in your Git repository!
#

import os
import re  # We use regular expressions to do more in-depth checks on generated HTML output from views.
import importlib
from rango.models import Category, Page
from populate_rango import populate
from django.urls import reverse
from django.test import TestCase
from django.db.models.query import QuerySet

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class Chapter6PopulationScriptTest(TestCase):
    """
    A few simple tests to examine whether the population script has been updated to include the requested changes (views for pages).
    """
    def setUp(self):
        populate()

    def test_page_objects_have_views(self):
        """
        Checks the basic requirement that all pages must have a positive view count.
        """
        pages = Page.objects.filter()
        for page in pages:
            self.assertTrue(
                page.views > 0,
                f"{FAILURE_HEADER}The page '{page.title}' has zero or negative views. Update populate_rango.py.{FAILURE_FOOTER}"
            )


class Chapter6IndexViewTests(TestCase):
    """
    A series of tests that examine the behaviour of the index view and its corresponding template.
    Tests to see if the context dictionary is correctly formed, and whether the response is correct.
    """
    def setUp(self):
        populate()
        self.response = self.client.get(reverse('rango:index'))
        self.content = self.response.content.decode()

    def test_template_filename(self):
        """
        Still using a template?
        """
        self.assertTemplateUsed(
            self.response, 'rango/index.html',
            f"{FAILURE_HEADER}Are you using index.html for the index() view?{FAILURE_FOOTER}"
        )

    def test_index_context_dictionary(self):
        """
        Runs some assertions to check if the context dictionary has the correct key/value pairings.
        """
        expected_boldmessage = 'Crunchy, creamy, cookie, candy, cupcake!'
        expected_categories = list(Category.objects.order_by('-likes')[:5])
        expected_pages = list(Page.objects.order_by('-views')[:5])

        self.assertTrue('boldmessage' in self.response.context)
        self.assertEqual(expected_boldmessage, self.response.context['boldmessage'])

        self.assertTrue('categories' in self.response.context)
        self.assertEqual(type(self.response.context['categories']), QuerySet)
        self.assertEqual(expected_categories, list(self.response.context['categories']))

        self.assertTrue('pages' in self.response.context)
        self.assertEqual(type(self.response.context['pages']), QuerySet)
        self.assertEqual(expected_pages, list(self.response.context['pages']))

    def test_index_categories(self):
        """
        Checks the response generated by the index() view -- does it render the categories correctly?
        """
        category_regexes = [
            (r'<li>\s*<a\s+href="/rango/category/python/">Python</a>\s*</li>', 'Python'),
            (r'<li>\s*<a\s+href="/rango/category/django/">Django</a>\s*</li>', 'Django'),
            (r'<li>\s*<a\s+href="/rango/category/other-frameworks/">Other Frameworks</a>\s*</li>', 'Other Frameworks'),
        ]

        for regex, name in category_regexes:
            self.assertTrue(re.search(regex, self.content),
                            f"{FAILURE_HEADER}Missing link for {name} category in index.html.{FAILURE_FOOTER}")

    def test_index_pages(self):
        """
        Checks the response generated by the index() view -- does it render the pages correctly?
        """
        page_regexes = {
            'Official Python Tutorial': r'<li>\s*<a\s+href="http://docs.python.org/3/tutorial/">Official Python Tutorial</a>\s*\(\d+ views\)\s*</li>',
            'How to Think like a Computer Scientist': r'<li>\s*<a\s+href="http://www.greenteapress.com/thinkpython/">How to Think like a Computer Scientist</a>\s*\(\d+ views\)\s*</li>',
            'Learn Python in 10 Minutes': r'<li>\s*<a\s+href="http://www.korokithakis.net/tutorials/python/">Learn Python in 10 Minutes</a>\s*\(\d+ views\)\s*</li>',
            'Official Django Tutorial': r'<li>\s*<a\s+href="https://docs.djangoproject.com/en/2.1/intro/tutorial01/">Official Django Tutorial</a>\s*\(\d+ views\)\s*</li>',
            'Django Rocks': r'<li>\s*<a\s+href="http://www.djangorocks.com/">Django Rocks</a>\s*\(\d+ views\)\s*</li>',
        }

        expected_pages = list(Page.objects.order_by('-views')[:5])
        for page in expected_pages:
            regex = page_regexes.get(page.title, None)
            if regex:
                self.assertTrue(re.search(regex, self.content),
                                f"{FAILURE_HEADER}Incorrect page list markup in index.html.{FAILURE_FOOTER}")

    def test_index_response_titles(self):
        """
        Checks whether the correct titles are used (including <h2> tags) for categories and pages.
        """
        self.assertIn('<h2>Most Liked Categories</h2>', self.content)
        self.assertIn('<h2>Most Viewed Pages</h2>', self.content)


class Chapter6CategoryViewTests(TestCase):
    """
    Tests for the show_category view and template.
    """
    def setUp(self):
        populate()
        self.response = self.client.get(
            reverse('rango:show_category', kwargs={'category_name_slug': 'other-frameworks'}))
        self.content = self.response.content.decode()

    def test_template_filename(self):
        """
        Still using a template?
        """
        self.assertTemplateUsed(self.response, 'rango/category.html')

    def test_context_dictionary(self):
        """
        Given the response, does the context dictionary match up with what is expected?
        """
        category = Category.objects.get(name='Other Frameworks')
        expected_pages = list(Page.objects.filter(category=category).order_by('-views'))  # FIXED ORDERING

        self.assertEqual(self.response.context['category'], category)
        self.assertEqual(list(self.response.context['pages']), expected_pages)

    def test_for_homepage_link(self):
        """
        Checks to see if a hyperlink to the homepage is present.
        """
        self.assertTrue(re.search(r'<a\s+href="/rango/">Home</a>', self.content),
                        "We couldn't find a well-formed hyperlink to the Rango homepage in your category.html template.")


class Chapter6BadCategoryViewTests(TestCase):
    """
    Tests for handling non-existent categories.
    """
    def test_malformed_url(self):
        """
        Tests to see whether the URL patterns have been correctly entered.
        """
        response = self.client.get('/rango/category/')
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_category(self):
        """
        Attempts to lookup a category that does not exist in the database and checks the response.
        """
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'nonexistent'}))
        self.assertIn('The specified category does not exist.', response.content.decode())

    def test_empty_category(self):
        """
        Adds a Category without pages; checks to see what the response is.
        """
        Category.objects.create(name='Empty Category')
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'empty-category'}))
        self.assertIn('<strong>No pages currently in category.</strong>', response.content.decode())
# Tango with Django 2 Progress Tests
# By Leif Azzopardi and David Maxwell
# With assistance from Enzo Roiz (https://github.com/enzoroiz)
#
# Chapter 6 -- Models, Templates and Views
# Last updated: October 15th, 2019
# Revising Author: David Maxwell
#

#
# In order to run these tests, copy this module to your tango_with_django_project/rango/ directory.
# Once this is complete, run $ python manage.py test rango.tests_chapter6
#
# The tests will then be run, and the output displayed -- do you pass them all?
#
# Once you are done with the tests, delete the module. You don't need to put it in your Git repository!
#

import os
import re  # We use regular expressions to do more in-depth checks on generated HTML output from views.
import importlib
from rango.models import Category, Page
from populate_rango import populate
from django.urls import reverse
from django.test import TestCase
from django.db.models.query import QuerySet

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class Chapter6PopulationScriptTest(TestCase):
    """
    A few simple tests to examine whether the population script has been updated to include the requested changes (views for pages).
    """
    def setUp(self):
        populate()

    def test_page_objects_have_views(self):
        """
        Checks the basic requirement that all pages must have a positive view count.
        """
        pages = Page.objects.filter()
        for page in pages:
            self.assertTrue(
                page.views > 0,
                f"{FAILURE_HEADER}The page '{page.title}' has zero or negative views. Update populate_rango.py.{FAILURE_FOOTER}"
            )


class Chapter6IndexViewTests(TestCase):
    """
    A series of tests that examine the behaviour of the index view and its corresponding template.
    Tests to see if the context dictionary is correctly formed, and whether the response is correct.
    """
    def setUp(self):
        populate()
        self.response = self.client.get(reverse('rango:index'))
        self.content = self.response.content.decode()

    def test_template_filename(self):
        """
        Still using a template?
        """
        self.assertTemplateUsed(
            self.response, 'rango/index.html',
            f"{FAILURE_HEADER}Are you using index.html for the index() view?{FAILURE_FOOTER}"
        )

    def test_index_context_dictionary(self):
        """
        Runs some assertions to check if the context dictionary has the correct key/value pairings.
        """
        expected_boldmessage = 'Crunchy, creamy, cookie, candy, cupcake!'
        expected_categories = list(Category.objects.order_by('-likes')[:5])
        expected_pages = list(Page.objects.order_by('-views')[:5])

        self.assertTrue('boldmessage' in self.response.context)
        self.assertEqual(expected_boldmessage, self.response.context['boldmessage'])

        self.assertTrue('categories' in self.response.context)
        self.assertEqual(type(self.response.context['categories']), QuerySet)
        self.assertEqual(expected_categories, list(self.response.context['categories']))

        self.assertTrue('pages' in self.response.context)
        self.assertEqual(type(self.response.context['pages']), QuerySet)
        self.assertEqual(expected_pages, list(self.response.context['pages']))

    def test_index_categories(self):
        """
        Checks the response generated by the index() view -- does it render the categories correctly?
        """
        category_regexes = [
            (r'<li>\s*<a\s+href="/rango/category/python/">Python</a>\s*</li>', 'Python'),
            (r'<li>\s*<a\s+href="/rango/category/django/">Django</a>\s*</li>', 'Django'),
            (r'<li>\s*<a\s+href="/rango/category/other-frameworks/">Other Frameworks</a>\s*</li>', 'Other Frameworks'),
        ]

        for regex, name in category_regexes:
            self.assertTrue(re.search(regex, self.content),
                            f"{FAILURE_HEADER}Missing link for {name} category in index.html.{FAILURE_FOOTER}")

    def test_index_pages(self):
        """
        Checks the response generated by the index() view -- does it render the pages correctly?
        """
        page_regexes = {
            'Official Python Tutorial': r'<li>\s*<a\s+href="http://docs.python.org/3/tutorial/">Official Python Tutorial</a>\s*\(\d+ views\)\s*</li>',
            'How to Think like a Computer Scientist': r'<li>\s*<a\s+href="http://www.greenteapress.com/thinkpython/">How to Think like a Computer Scientist</a>\s*\(\d+ views\)\s*</li>',
            'Learn Python in 10 Minutes': r'<li>\s*<a\s+href="http://www.korokithakis.net/tutorials/python/">Learn Python in 10 Minutes</a>\s*\(\d+ views\)\s*</li>',
            'Official Django Tutorial': r'<li>\s*<a\s+href="https://docs.djangoproject.com/en/2.1/intro/tutorial01/">Official Django Tutorial</a>\s*\(\d+ views\)\s*</li>',
            'Django Rocks': r'<li>\s*<a\s+href="http://www.djangorocks.com/">Django Rocks</a>\s*\(\d+ views\)\s*</li>',
        }

        expected_pages = list(Page.objects.order_by('-views')[:5])
        for page in expected_pages:
            regex = page_regexes.get(page.title, None)
            if regex:
                self.assertTrue(re.search(regex, self.content),
                                f"{FAILURE_HEADER}Incorrect page list markup in index.html.{FAILURE_FOOTER}")

    def test_index_response_titles(self):
        """
        Checks whether the correct titles are used (including <h2> tags) for categories and pages.
        """
        self.assertIn('<h2>Most Liked Categories</h2>', self.content)
        self.assertIn('<h2>Most Viewed Pages</h2>', self.content)


class Chapter6CategoryViewTests(TestCase):
    """
    Tests for the show_category view and template.
    """
    def setUp(self):
        populate()
        self.response = self.client.get(
            reverse('rango:show_category', kwargs={'category_name_slug': 'other-frameworks'}))
        self.content = self.response.content.decode()

    def test_template_filename(self):
        """
        Still using a template?
        """
        self.assertTemplateUsed(self.response, 'rango/category.html')

    def test_context_dictionary(self):
        """
        Given the response, does the context dictionary match up with what is expected?
        """
        category = Category.objects.get(name='Other Frameworks')
        expected_pages = list(Page.objects.filter(category=category).order_by('-views'))  # FIXED ORDERING

        self.assertEqual(self.response.context['category'], category)
        self.assertEqual(list(self.response.context['pages']), expected_pages)

    def test_for_homepage_link(self):
        """
        Checks to see if a hyperlink to the homepage is present.
        """
        self.assertTrue(re.search(r'<a\s+href="/rango/">Home</a>', self.content),
                        "We couldn't find a well-formed hyperlink to the Rango homepage in your category.html template.")


class Chapter6BadCategoryViewTests(TestCase):
    """
    Tests for handling non-existent categories.
    """
    def test_malformed_url(self):
        """
        Tests to see whether the URL patterns have been correctly entered.
        """
        response = self.client.get('/rango/category/')
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_category(self):
        """
        Attempts to lookup a category that does not exist in the database and checks the response.
        """
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'nonexistent'}))
        self.assertIn('The specified category does not exist.', response.content.decode())

    def test_empty_category(self):
        """
        Adds a Category without pages; checks to see what the response is.
        """
        Category.objects.create(name='Empty Category')
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'empty-category'}))
        self.assertIn('<strong>No pages currently in category.</strong>', response.content.decode())
