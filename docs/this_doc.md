# Automatic documentation generated with mkdocs

[Mkdocs](https://www.mkdocs.org/) is used in combination with [mkdocstrings](https://mkdocstrings.github.io/) to automatically generate this documentation for the python classes and functions.

The mkdocs configuration file can be found here: `mkdocs.yml`  
The documentation files used to build the site can be found here: `docs/.`

## Build the documentation

To build the documentation in a custom destination folder:
`mkdocs build --site-dir <destination-folder>`
The default folder is `site`

## serve the documentation with mkdocs

`mkdocs serve`

For this to work you either have to install mkdocs and its requirements locally or connect the  workspace in your IDE to the `server` docker/podman container.

## Add a new python file to the documentation:

- Create a new file `<django-app-name>_<python-file-name>.md` in `docs/.`
- Edit this new file and add:
    - `## <django-app-name>.<python-file-name>` Subtitle for this section
    - `::: <django-app-name>.<python-file-name>` The python file that will be read
    - More than one python file can be added to a single mkdocs `.md` file if needed 
- Add this file to to the mkdocs config file `mkdocs.yml`
    - `- <title>: '<django-app-name>_<python-file-name>.md'`

## Guideline for writing docstrings

```
    """Description of the class or function    

    Args:
        Param: description (The type will be read from the function definition)

    Attributes:
        attr (type): description (For django models add the type here in the docstring)

    Returns:
        description (The type will be read from the function definition)

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
