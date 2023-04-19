# organizer-app
- [settings_added branch](https://github.com/audreytracy/organizer-app/tree/settings_added) has added settings page, used global variable in views to pass user_id between views, not sure that's the best practice..  
    ``` git clone -b settings_added https://github.com/audreytracy/organizer-app.git ``` 
    - ```href=""``` should be replaced with ```href = "{% url 'url_path_name' %}"``` when to-do and create event are implemented (in settings.html nav bar and other templates since nav bar will also probably end up in the other templates):  
    ```
    <a class="btn btn-secondary" href="">to-do</a>
    <a class="btn btn-secondary" href="">create event</a>
    ```
    

- [main branch](https://github.com/audreytracy/organizer-app/) requires pull request to merge  
I think once we merge to main we can mark the task as done (like as far as trello stuff goes)
