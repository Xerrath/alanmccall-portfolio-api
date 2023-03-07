# Alans custom Portfolio Backend API

_A api session for Portfolio Building_

    ## API

        ### Admin Create

            A user can create a Admin instance, storing users name, email, password, and auto generates a id

            Endpoint: '/admin/add'
            Method: 'POST'

            Expected Response in JSON:

            {
                'admin_id':: INT
                'admin_pw': STR
                'admin_name': STR
                'admin_email': STR
            }

        ### Grab All Admin's Information

            A user can Grab all Admins instance

            Endpoint: '/admin'
            Method: 'GET'

            Expected Response in JSON:

            {
                [
                    'admin_id':: INT
                    'admin_name': STR
                    'admin_email': STR
                ]
            }

        ### Delete Admin

            A user can delete a Admin instance by passing in the admin_id

            Endpoint: '/admin/delete/<admin_id>'
            Method: 'DELETE'

            Expected Response in JSON:

            {
                "The slected Admin has been deleted"
            }

        ### Create Blog

            A Admin can create a Blog instance, storing 

            Endpoint: '/blog/add'
            Method: 'POST'

            Expected Response in JSON:

            {
                'blog_thumb_img': utf-8 BYTE
                'blog_hero_img': utf-8 BYTE
                'blog_title': STR
                'blog_contents': TEXT
                'blog_date': DATE
                'blog_admin_id': INT
            }

        ### Grab All Blogs

            A Admin can grab all blogs instance accross all Admins

            Endpoint: '/admin'
            Method: 'GET'

            Expected Response in JSON:

            {
                [
                    'blog_thumb_img': utf-8 BYTE
                    'blog_hero_img': utf-8 BYTE
                    'blog_title': STR
                    'blog_contents': TEXT
                    'blog_date': DATE
                    'blog_admin_id': INT
                ]
            }

        ### Delete Blog

            A Admin can delete a blog instance by passing in the blog_id

            Endpoint: '/blog/delete/<id>'
            Method: 'DELETE'

            Expected Response in JSON:

            {
                "The selected blog has been deleted"
            }

        ### Get Blog by ID

            A admin user can edit a blog details by a certain blog_id

            Endpoint: '/blog/edit/<int:id>'
            Method: 'POST'

            Expected Response in JSON:

            {
                'blog_thumb_img': utf-8 BYTE
                'blog_hero_img': utf-8 BYTE
                'blog_title': STR
                'blog_contents': TEXT
                'blog_date': DATE
                'blog_admin_id': INT
            }

        ### Get Blogs By Admin's Relation

            A admin can get all Blogs related by the admin by passing admin_id

            Endpoint: '/get/blogs/by/<int:blog_admin_id>'
            Method: 'GET'

            Expected Response in JSON:

            {
                'blog_thumb_img': utf-8 BYTE
                'blog_hero_img': utf-8 BYTE
                'blog_title': STR
                'blog_contents': TEXT
                'blog_date': DATE
                'blog_admin_id': INT
            }

        ### Get All Projects

            A admin can grab all Projects

            Endpoint: '/get/projects'
            Method: 'GET'

            Expected Response in JSON:

            {
                [
                    'project_thumb_img': utf-8 BYTE
                    'project_logo_img': utf-8 BYTE
                    'project_hero_img': utf-8 BYTE
                    'project_title': STR
                    'project_language': STR
                    'project_development_type': STR
                    'project_description': TEXT
                    'project_url': STR
                ]
            }

        ### Get All Projects Related to Admin

            A admin can grab all Projects related to a admin by passing the admin_id

            Endpoint: '/get/projects/by/<int:project_admin_id>'
            Method: 'GET'

            Expected Response in JSON:

            {
                [
                    'project_thumb_img': utf-8 BYTE
                    'project_logo_img': utf-8 BYTE
                    'project_hero_img': utf-8 BYTE
                    'project_title': STR
                    'project_language': STR
                    'project_development_type': STR
                    'project_description': TEXT
                    'project_url': STR
                ]
            }
        
        ### Edit a Project

            A admin can edit a project by passing the project_id

            Endpoint: '/project/edit/<int:project_id>'
            Method: 'POST'

        ### Grab a Project

            A admin can edit a project by passing the project_id

            Endpoint: '/project/<id>'
            Method: 'GET'

        ### Delete a Project

            A admin can delete a project by passing the project_id

            Endpoint: '/project/<id>'
            Method: 'DELETE'

            Expected Response in JSON:

            {
                "The selected project has been deleted"
            }

        ### Create a Project

            A admin can create a project

            Endpoint: '/project/add'
            Method: 'POST'

            Expected Response in JSON:

            {
                'project_thumb_img': utf-8 BYTE
                'project_logo_img': utf-8 BYTE
                'project_hero_img': utf-8 BYTE
                'project_title': STR
                'project_language': STR
                'project_development_type': STR
                'project_description': TEXT
                'project_url': STR
            }

        ### Grab all Users

            A admin can grab all users

            Endpoint: '/users'
            Method: 'GET'

            Expected Response in JSON:

            {
                [
                    'user_id': INT
                    'user_email': STR
                    'user_name': STR
                    'user_url': STR
                    'user_admin_id': INT
                ]
            }

        ### Grab all Users By admin relation

            A admin grab all user by relation by passing the admnin_id

            Endpoint: '/get/all/users/<int:user_admin_id>'
            Method: 'GET'

            Expected Response in JSON:

            {
                [
                    'user_id': INT
                    'user_email': STR
                    'user_name': STR
                    'user_url': STR
                    'user_admin_id': INT
                ]
            }

        ### Grab A user

            A admin grab a user by user_id

            Endpoint: '/users/<int:user_id>'
            Method: 'GET'

            Expected Response in JSON:

            {
                'user_id': INT
                'user_email': STR
                'user_name': STR
                'user_url': STR
                'user_admin_id': INT
            }

        ### Edit A user

            A admin can edit a user by passing user_id

            Endpoint: '/users/edit/<int:user_id>'
            Method: 'POST'

            Expected Response in JSON:

            {
                'user_id': INT
                'user_email': STR
                'user_name': STR
                'user_pw': STR
                'user_url': STR
                'user_admin_id': INT
            }

        ### Delete A user

            A admin can delete a user by passing user_id

            Endpoint: '/users/delete/<int:user_id>'
            Method: 'DELETE'


            Expected Response in JSON:

            {
                'The selected user has been deleted'
            }

        ### Create A user

            A admin can create a user

            Endpoint: '/user/add'
            Method: 'POST'

            Expected Response in JSON:

            {
                'user_id': INT
                'user_email': STR
                'user_name': STR
                'user_pw': STR
                'user_url': STR
                'user_admin_id': INT
            }

        ### Get Testimonials by admin relation

            A admin can grab all testimonials by passing admin_id

            Endpoint: '/get/testimonials/by/admin/relation/<int:id>'
            Method: 'GET'

            Expected Response in JSON:

            {
                [
                    'testimonial_id': INT
                    'testimonial_review': TEXT
                    'testimonial_published': Boolean
                    'testimonial_id_users': INT
                    'testimonial_admin_id': INT
                ]
            }

        ### Get Testimonials by user relation

            A user can grab all testimonials by passing user_id

            Endpoint: '/get/testimonials/by/user/relation/<int:testimonial_id_users>'
            Method: 'GET'

            Expected Response in JSON:

            {
                [
                    'testimonial_id': INT
                    'testimonial_review': TEXT
                    'testimonial_published': Boolean
                    'testimonial_id_users': INT
                    'testimonial_admin_id': INT
                ]
            }

        ### Get Testimonials by id

            A admin or user can grab a testimonial by passing testimonial_id

            Endpoint: '/testimonial/<int:id>'
            Method: 'GET'

            Expected Response in JSON:

            {
                'testimonial_id': INT
                'testimonial_review': TEXT
                'testimonial_published': Boolean
                'testimonial_id_users': INT
                'testimonial_admin_id': INT
            }

        ### Delete Testimonials by id

            A admin or user can delete a testimonial by passing testimonial_id

            Endpoint: '/testimonial/<int:id>'
            Method: 'DELETE'

            Expected Response in JSON:

            {
                'The selected Testimony has been deleted'
            }
        
        ### Create a Testimonial

            A user can create a Testimonial

            Endpoint: '/testimonial/add'
            Method: 'POST'

            Expected Response in JSON:

            {
                'testimonial_review': TEXT
                'testimonial_published': Boolean
                'testimonial_id_users': INT
                'testimonial_admin_id': INT
            }

        ### Edit a Testimonial

            A user or admin can edit a Testimonial by testomial_id

            Endpoint: '/testimonial/add'
            Method: 'POST'

            Expected Response in JSON:

            {
                'testimonial_id': INT
                'testimonial_review': TEXT
                'testimonial_published': Boolean
                'testimonial_id_users': INT
                'testimonial_admin_id': INT
            }

        ### A user can login and get a JWT
            once a user is verified and logged in the JWT will be made and it will pass in:

            {
                'email': STR
                'user_id': INT
                'user_admin_id': INT
                'user_logged_in' = 'USER'
            }

            #The verify process needs

            Endpoint: '/log/verify/user'
            Method: 'POST'

            Expected Response in JSON:

            {
                'email': STR
                'pw': STR
            }

        ### A Admin can login and get a JWT
            once a user is verified and logged in the JWT will be made and it will pass in:

            {
                'email': STR
                'admin_auth_id': INT
                'user_logged_in' = 'ADMIN'
            }

            #The verify process needs

            Endpoint: '/log/verify/admin'
            Method: 'POST'

            Expected Response in JSON:

            {
                'email': STR
                'pw': STR
            }


###### Created By Alan McCall | Capstone Project