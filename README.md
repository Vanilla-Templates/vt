### What is `Vanilla Template`?

Vanilla Template is a templating mark-up language and a static-site generator (SSG) in python.

### Why `Vanilla Template`?

In this new age of web development, and particularly in the front-end side, we are bombarded with a plethora of options in the form of frameworks, tools and technologies which cut across client-side rendering, server-side rendering and what have you. A good example is `React`, which has become the most popular front-end library in many companies, big and small alike.

As a passinate developer who regularly makes websites ranging from fun silly websites all the way to full stack dynamic websites, we get to play around with these tools as we learn, and in the process discover what we like and what we don't like.

Sometimes you need a full-on framework like `NextJS` or go the vanilla route (raw html, css and Javascript). I took it upon myself to bridge this gap by creating Vanilla Templates, a templating language which isn't coupled to any framework or library (kind of `jinja 2` is coupled with python Flask).

## Installation

* create a working directory and `cd` into it

```
mkdir vanilla
cd vanilla
```

* degit from gh in dir

```
pip install git+https://github.com/FREDRICKKYEKI/vanilla-templates.git
```

* create .gitignore in working directory and add into it.
* create public directory (`NOTE:` **We insist you call it public**) for static files.

```
mkdir public
```

* create an `index.html` and start creating `vanilla templates`

### Example of a vanilla template component:

```
<vt_user name="Alison Bob" age="33" role="Admin" />
```

### How to fill a component:

- normal props
- dict (with '{prop: value}' schema)
- map from list attr into component list[dict]
- map from file into component (with list[dict] schema)
- map from api into component (with list[dict] schema)

## passing data to tags

- regular html attributes
- mapping data from list/array
  - vt:map-from (map from list)
  - vt:map-from-file
  - vt:map-from-api
- (dict or str or int but not iterable objects)
  - vt:from
  - vt:from-file
  - vt:from-api
  - vt:from

## Property accessor using ':'

You can access data using the property accessor ':' from a or file, api as a key.

**NOTE**: It only goes to one level
