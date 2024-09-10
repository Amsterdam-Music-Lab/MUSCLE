# Automatic documentation generated with mkdocs

[Mkdocs](https://www.mkdocs.org/) is used in combination with [mkdocstrings](https://mkdocstrings.github.io/) to automatically generate this documentation for the python classes and functions.

The mkdocs configuration file can be found here: `backend/mkdocs.yml`  
The documentation files used to build the site can be found here: `backend/docs/.`

## Build the documentation

To build the documentation in a custom destination folder:
`mkdocs build --site-dir <destination-folder>`
The default folder is `backend/site`

## serve the documentation with mkdocs

`mkdocs serve --dev-addr localhost:8080`

For this to work you either have to install mkdocs and its requirements locally or connect the  workspace in your IDE to the `server` docker/podman container.

## Add a new python file to the documentation:

- Create a new file `<django-app-name>_<python-file-name>.md` in `backend/docs/.`
- Edit this new file and add:
    - `## <django-app-name>.<python-file-name>` Subtitle for this section
    - `::: <django-app-name>.<python-file-name>` The python file that will be read
    - More than one python file can be added to a single mkdocs `.md` file if needed 
- Add this file to to the mkdocs config file `backend/mkdocs.yml`
    - `- <title>: '<django-app-name>_<python-file-name>.md'`

## Guideline for writing docstrings

```
    """Description of the class or function    

    Args:
        Param (type): description

    Attributes:
        attr (type): description

    Returns:
        (type): description

    Raises:
        Error-code: description

    Note:
        Optional note

    Example:
        Examples should be written in doctest format, and should illustrate how
        to use the function.
    """
```

[Click here to read more about formatting docstrings](https://realpython.com/python-project-documentation-with-mkdocs/#step-3-write-and-format-your-docstrings)
