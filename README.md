# Vanilla Templates

![](images/logo_bg.jpg)

[❤ Support vt](https://www.buymeacoffee.com/fredrickkyeki)

Latest version:   `1.0.0`

[](https://github.com/vanilla-templates/vt_docs)

*   [Getting Started](#getting-started)
    *   [Installation](#installation)
*   [Usage - How `vt` works](#usage)
    *   [vt\_imports](#vt_imports)
*   [Passing data to `vt` components:](#passing-data-to-components)
    *   [Using regular `vt` props](#regular-vt-props)
    *   [vt:from](#vt:from)
    *   [vt:from-file](#vt:from-file)
    *   [vt:from-md](#vt:from-md)
    *   [vt:from-api](#vt:from-api)
    *   [Mapping over a list of data:](#mapping-over-data)
    
    *   [vt:map-from](#vt:map-from)
    *   [vt:map-from-file](#vt:map-from-file)
    *   [vt:map-from-api](#vt:map-from-api)
    
*   [Prop Accessor '::'](#prop-accessor)
    *   `` `json-file::prop` ``
    *   `` `api::prop` ``
*   [Other vt Features](#other-features)
    *   [In-place components](#in-place-components)
*   [Special 'vt' atributes and tags:](#special-attrs-and-tags)
    *   [vt:parent](#vt:parent)
    *   [vt\_child](#vt_child)
    *   [vt\_frag](#vt_frag)
*   [Static Site Generation](#SSG)
    *   `python3 -m vt.build`
*   [Server Side Rendering](#SSR)
    *   `python3 -m vt.serve`

### What is `Vanilla Templates`?

    `<vt_user name="Alison Bob" age="33" role="Admin" />`
  

`Vanilla Templates` is a:

1.  Templating mark-up language,
2.  Static Site Generator (SSG)
3.  and a Server Side Rendering (SSR) engine.

developed in `Python`.

### Why `Vanilla Templates`?

In this new age of web development, and particularly in the front-end side, we are bombarded with a plethora of options in the form of frameworks, tools and technologies which cut across client-side rendering, server-side rendering and what have you. A good example is `React`, which has become the most popular front-end.

As a passinate developer who regularly makes websites ranging from fun silly websites, all the way to full stack dynamic websites, we get to play around with these tools as we learn, and in the process discover what we like and what we don't like.

Sometimes you need a full-on framework like `NextJS` or go the vanilla route (raw html, css and Javascript). I took it upon myself to bridge this gap by creating `Vanilla Templates`, a templating language which isn't coupled to any framework or library (kind of how `jinja 2` is coupled with `Flask`).

* * *

Installation
------------

1.  Create a working directory and `cd` into it.
    
    `mkdir vanilla-test   cd vanilla-test`
    
2.  pip install the package from github into the working directory:
    
    `pip install git+https://github.com/vanilla-templates/vt.git`
3.  Create `.gitignore` in working directory and add the `vt` folder into it.
4.  create public directory (`NOTE:` **We insist you call it public**) for static files.

`mkdir public`

6.  create an `index.html` and start creating `vanilla templates`
7.  Build or serve your work on a pre-configured port (**2220**).  
    `python -m vt.serve` - for serving  
    `python -m vt.building` - for generating static site in the build directory

* * *

### How `vt` works:

The first step to using `vt` is to first create the components you will use to fill with data:

For example:

        `<div class="blog__card" >             <div class="card__header">               <h3>{title}</h3>             </div>             <div class="card__desc">               <p>{description}</p>             <div/>             <span class="card__footer" >               <small>{date}</small> | <small>{about}</small> |               <small> <i class="icon-bubble3"></i>{readers}</small>             </span>             </div>           </div>`
        

Notice the placeholders wrapped in `` `{*}` ``. As the template above suggests, it requires 5 data points, namely:

*   title
*   description
*   about
*   date
*   readers

Let's look at some ways we can populate the data into the template and into the final html file. For this, let's assume our `index.html` looks like this:

* * *

### `vt_imports`

The first special attribute we'll look into is the `vt_imports="[*]"` attribute.

        `<!DOCTYPE html>           <html lang="en" vt_imports="['components/vt_blog.html']">             <head>               <meta charset="UTF-8" />               <meta name="viewport" content="width=device-width, initial-scale=1.0" />               <title>Vanilla</title>             </head>             <body>                   <vt_blog                     title="Vanilla rocks!!!"                     about="vanilla templates"                     date="1/1/24"                     readers="1000"                     description="This is a blog about Vanilla Templates"                   />             </body>           </html>`
        
      

This is a special `vt` attribute which informs the engine of an existence of a `vt` component.

A few things to note here:

*   The naming convention (prefix `'vt_'` in the component name).

*   The engine will still parse the vt components with the prefix, but it is `highly recommended` that you add the prefix so that the the templating engine picks it up while cleaning up and subsequently alert you incase you forgot to import it (more on this later).
*   Every imported component `MUST` be used in the parent component otherwise the engine `throws an Exception.`

*   Since it's the first time to come across this attribute, the following is to be said about it:

*   Any component to be used on any template `MUST` be imported using the `vt_imports` attribute
*   The attributes takes in a list of paths.
`**IMPORTANT** The paths in the list are not relative to the template, they are relative to the root directory: i.e, if your template is in 'components/vt_header.html' and is importing another template in 'components/logo.html', the vt_imports of the 'vt_header' component should be 'vt_imports=["components/vt_logo.html"]'`

* * *

### How to pass data to a component:

Now that we have understood how to import a component into another component, let's see the various methods of passing data into the component without having to repeat yourself(or copy and pasting).  
  

1.  #### Regular html attributes (or props in this `vt` terms)
    
    Data can be passed to the template through regular html attributes, also called `vt props` (properties in full).
    
          `<vt_blog               title="Vanilla rocks!!!"               about="vanilla templates"               date="'1/1/24'"               readers="1000"               description="This is a blog about Vanilla Templates"             />`
          
      
    
    A few pointers when using this method of passing data:
    
    *   Each attribute `MUST MATCH` the template place holder. Notice the placeholders in [this](#vt_template) template match with the props in the component above.
    *   For native html attributes, we suggest that you add a unique prefix/suffix for the engine to parse it correctly:
        *   e.g instad of `<vt_blog class="card"/>` ,  
            we suggest `<vt_blog class_="card"/>`  
            or `<vt_blog _class="card"/>`
    *   Notice the `date="'1/1/24'"`:
        *   Since the the value is directly evaluated into python, the extra `''` aid the compiler to know that its a string and not an int (expression).
    *   Lastly, the data passed this way is not processed in any way and is injected as is.
    
    This is the rendered card (`find the code to this in the [github](https://github.com/vanilla-templates/vt_docs) repo):`
    
    ### Vanilla rocks!!!
    
    This is a blog about Vanilla Templates
    
    1/1/24 | vanilla templates | 1000
    
2.  #### Using `vt:from` special attribute:
    
    The `vt:from` prop accepts a `key-value like` json text, which is parsed into a `python dictionary`.
    
          `<vt_blog  vt:from='{"title":"Vanilla rocks!!!",                                    "about":"vanilla templates,                                    "date":"1/1/24,                                    "readers":"1000,                                    "description":"This is a blog about Vanilla Templates"                                  }'             />`
          
      
    
    Pointers to this method:
    
    1.  The inner quotes `MUST` be `double quotes.` Failure to this will result in the engine
    
    i.e,*   `vt:from='{"key":"value"}'`✅
    These are wrong:*   `vt:from="{'key':'value'}"`❌
    *   `vt:from="{"key":"value"}"`❌
    *   `vt:from="{'key':"value"}"`❌
    *   `vt:from="{"key":'value'}"`❌
    `throwing an exception`.
    
    3.  Just with regular props, the keys `MUST` match with the placeholders in the [template.](#vt_template)
    
    This is the rendered card (`find the code to this in the [github](https://github.com/vanilla-templates/vt_docs) repo):`
    
    ### Vanilla rocks!!!
    
    This is a blog about Vanilla Templates
    
    1/1/24 | vanilla templates | 1000
    
3.  #### `vt:from-file`
    
    Here is where `vt` starts to become interesting:
    
    The `vt:from-file` prop accepts a `file path` which contains a `json file`, which, just like above, is parsed into a `python dictionary`.
    
    Say we have a `file.json` in our root directory, which contains:
    
        `{             "title":"Vanilla rocks!!!",             "about":"vanilla templates",             "date":"1/1/24",             "readers":"1000",             "description":"This is a blog about Vanilla Templates"         }`
        
      
    
    This is how you would render the template:
    
        `<vt_test_card vt:from-file="file.json" />`
        
      
    
    This is the rendered card (`find the code to this in the [github](https://github.com/vanilla-templates/vt_docs) repo):`
    
    ### Vanilla rocks!!!
    
    This is a blog about Vanilla Templates
    
    1/1/24 | vanilla templates | 1000
    
4.  #### `vt:from-md`:
    
    The `vt:from-md` allows the `vt` compiler to read a markdown file into a tag.
    
        `<vt_frag vt:from-md="sample.md" />`
        
      
    
    This is the rendered markdown text:
    
    This is a sample markdown text
    ------------------------------
    
    The `vt_frag` tag is a special `vt` tag used when you don't want to render a certain tag on the final html (more on this later).
    
    If you want the tag to remain after you inject the markdown text, you can use a native html tag, as shown below.
    
        `<div vt:from-md="sample.md"> </div>`
        
      
    
5.  #### `vt:from-api`:
    
    The `vt:from-api` from the name, makes a request and fills a `vt` template with the data.
    
    For example:
    
        `<vt_cat_card vt:from-api="https://catfact.ninja/fact" />`
        
      
    
    The actual template looks like this:
    
        `<div class="card">         <div class="card-header">           <strong>Cat fax ! </strong>         </div>         <div class="card-body">           <strong>Fact: </strong>{fact}         </div>         <div class="card-footer">           <strong>Length: </strong>{length}         </div>       </div>`
        
      
    
    This is the rendered card from the api: [https://catfact.ninja/fact](https://catfact.ninja/fact).
    
    **Cat fax !**
    
    **Fact:** Female cats tend to be right pawed, while male cats are more often left pawed. Interestingly, while 90% of humans are right handed, the remaining 10% of lefties also tend to be male.
    
    **Length:** 182
    
6.  ##### Mapping over data records
    
    Every once in a while you'll need to create `html` elements which have recurring properties, and without a proper programmatic framework, you'll be forced to write the same pieces of text over and over.
    
    With a variety of the mapping tags that `vt` provides, you can map over a `list of dictionaries` (in `json format`) without having to copy and paste the same element over and again.
    
    *   #### `vt:map-from`
        
        The first attribute in in the special suite of the mapping attributes is `vt:map-from`, which as stated above, takes in a list of json objects (parsed to dicts in python).
        
        For example, consider the component:
        
                `<vt_posts vt:map-from='[{                 "userId": 1,                 "id": 1,                 "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",                 "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"                 }, {                 "userId": 1,                 "id": 2,                 "title": "qui est esse",                 "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"                 }, {                 "userId": 1,                 "id": 3,                 "title": "ea molestias quasi exercitationem repellat qui ipsa sit aut",                 "body": "et iusto sed quo iure\nvoluptatem occaecati omnis eligendi aut ad\nvoluptatem doloribus vel accusantium quis pariatur\nmolestiae porro eius odio et labore et velit aut"                 }]' />`
                
            
        
        and its corresponding template below:
        
            `<div class="card m-2 p-2">         <div class="card-header">           <h3>{title}</h3>         </div>         <div class="card-body">             <div>UserId: {userId}</div>             <p>{body}</p>         </div>         <div class="card-footer">             <small>id: {id}</small>         </div>       </div>`
        
            
          
        
        These are rendered cards (`find the code to this in the [github](https://github.com/vanilla-templates/vt_docs) repo)`:
        
        ### sunt aut facere repellat provident occaecati excepturi optio reprehenderit
        
        UserId: 1
        
        quia et suscipit suscipit recusandae consequuntur expedita et cum reprehenderit molestiae ut ut quas totam nostrum rerum est autem sunt rem eveniet architecto
        
        id: 1
        
        ### qui est esse
        
        UserId: 1
        
        est rerum tempore vitae sequi sint nihil reprehenderit dolor beatae ea dolores neque fugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis qui aperiam non debitis possimus qui neque nisi nulla
        
        id: 2
        
        ### ea molestias quasi exercitationem repellat qui ipsa sit aut
        
        UserId: 1
        
        et iusto sed quo iure voluptatem occaecati omnis eligendi aut ad voluptatem doloribus vel accusantium quis pariatur molestiae porro eius odio et labore et velit aut
        
        id: 3
        
        ### eum et est occaecati
        
        UserId: 1
        
        ullam et saepe reiciendis voluptatem adipisci sit amet autem assumenda provident rerum culpa quis hic commodi nesciunt rem tenetur doloremque ipsam iure quis sunt voluptatem rerum illo velit
        
        id: 4
        
        ### nesciunt quas odio
        
        UserId: 1
        
        repudiandae veniam quaerat sunt sed alias aut fugiat sit autem sed est voluptatem omnis possimus esse voluptatibus quis est aut tenetur dolor neque
        
        id: 5
        
    *   #### `vt:map-from-file`
        
        From the name, `vt:map-from-file` maps list data from a `json` file into a template.
        
        Given that we have a `file.json` in the root directory:
        
                `[             {                 "userId": 1,                 "id": 1,                 "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",                 "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"             },             {                 "userId": 1,                 "id": 2,                 "title": "qui est esse",                 "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"             },             {                 "userId": 1,                 "id": 3,                 "title": "ea molestias quasi exercitationem repellat qui ipsa sit aut",                 "body": "et iusto sed quo iure\nvoluptatem occaecati omnis eligendi aut ad\nvoluptatem doloribus vel accusantium quis pariatur\nmolestiae porro eius odio et labore et velit aut"             }         ]`
                
            
        
        and a component:
        
                `<vt_posts vt:map-from-file="list.json" />`
                
            
        
        This is the rendered list (represented inside `vt` templates):
        
        ### sunt aut facere repellat provident occaecati excepturi optio reprehenderit
        
        UserId: 1
        
        quia et suscipit suscipit recusandae consequuntur expedita et cum reprehenderit molestiae ut ut quas totam nostrum rerum est autem sunt rem eveniet architecto
        
        id: 1
        
        ### qui est esse
        
        UserId: 1
        
        est rerum tempore vitae sequi sint nihil reprehenderit dolor beatae ea dolores neque fugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis qui aperiam non debitis possimus qui neque nisi nulla
        
        id: 2
        
        ### ea molestias quasi exercitationem repellat qui ipsa sit aut
        
        UserId: 1
        
        et iusto sed quo iure voluptatem occaecati omnis eligendi aut ad voluptatem doloribus vel accusantium quis pariatur molestiae porro eius odio et labore et velit aut
        
        id: 3
        
    *   #### `vt:map-from-api`:
        
        The `vt:map-from-api` makes a request and fills a `vt` template with the data (`data MUST be in list/array formart`).
        
                `<vt_posts vt:map-from-api="https://jsonplaceholder.typicode.com/posts" />`
                
            
        
        This is the rendered list (represented inside `vt` templates):
        
        ### sunt aut facere repellat provident occaecati excepturi optio reprehenderit
        
        UserId: 1
        
        quia et suscipit suscipit recusandae consequuntur expedita et cum reprehenderit molestiae ut ut quas totam nostrum rerum est autem sunt rem eveniet architecto
        
        id: 1
        
        ### qui est esse
        
        UserId: 1
        
        est rerum tempore vitae sequi sint nihil reprehenderit dolor beatae ea dolores neque fugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis qui aperiam non debitis possimus qui neque nisi nulla
        
        id: 2
        
        ### ea molestias quasi exercitationem repellat qui ipsa sit aut
        
        UserId: 1
        
        et iusto sed quo iure voluptatem occaecati omnis eligendi aut ad voluptatem doloribus vel accusantium quis pariatur molestiae porro eius odio et labore et velit aut
        
        id: 3
        
        ### eum et est occaecati
        
        UserId: 1
        
        ullam et saepe reiciendis voluptatem adipisci sit amet autem assumenda provident rerum culpa quis hic commodi nesciunt rem tenetur doloremque ipsam iure quis sunt voluptatem rerum illo velit
        
        id: 4
        
        ### nesciunt quas odio
        
        UserId: 1
        
        repudiandae veniam quaerat sunt sed alias aut fugiat sit autem sed est voluptatem omnis possimus esse voluptatibus quis est aut tenetur dolor neque
        
        id: 5
        
        ### dolorem eum magni eos aperiam quia
        
        UserId: 1
        
        ut aspernatur corporis harum nihil quis provident sequi mollitia nobis aliquid molestiae perspiciatis et ea nemo ab reprehenderit accusantium quas voluptate dolores velit et doloremque molestiae
        
        id: 6
        
        ### magnam facilis autem
        
        UserId: 1
        
        dolore placeat quibusdam ea quo vitae magni quis enim qui quis quo nemo aut saepe quidem repellat excepturi ut quia sunt ut sequi eos ea sed quas
        
        id: 7
        
        ### dolorem dolore est ipsam
        
        UserId: 1
        
        dignissimos aperiam dolorem qui eum facilis quibusdam animi sint suscipit qui sint possimus cum quaerat magni maiores excepturi ipsam ut commodi dolor voluptatum modi aut vitae
        
        id: 8
        
        ### nesciunt iure omnis dolorem tempora et accusantium
        
        UserId: 1
        
        consectetur animi nesciunt iure dolore enim quia ad veniam autem ut quam aut nobis et est aut quod aut provident voluptas autem voluptas
        
        id: 9
        
        ### optio molestias id quia eum
        
        UserId: 1
        
        quo et expedita modi cum officia vel magni doloribus qui repudiandae vero nisi sit quos veniam quod sed accusamus veritatis error
        
        id: 10
        
        ### et ea vero quia laudantium autem
        
        UserId: 2
        
        delectus reiciendis molestiae occaecati non minima eveniet qui voluptatibus accusamus in eum beatae sit vel qui neque voluptates ut commodi qui incidunt ut animi commodi
        
        id: 11
        
        ### in quibusdam tempore odit est dolorem
        
        UserId: 2
        
        itaque id aut magnam praesentium quia et ea odit et ea voluptas et sapiente quia nihil amet occaecati quia id voluptatem incidunt ea est distinctio odio
        
        id: 12
        
        ### dolorum ut in voluptas mollitia et saepe quo animi
        
        UserId: 2
        
        aut dicta possimus sint mollitia voluptas commodi quo doloremque iste corrupti reiciendis voluptatem eius rerum sit cumque quod eligendi laborum minima perferendis recusandae assumenda consectetur porro architecto ipsum ipsam
        
        id: 13
        
        ### voluptatem eligendi optio
        
        UserId: 2
        
        fuga et accusamus dolorum perferendis illo voluptas non doloremque neque facere ad qui dolorum molestiae beatae sed aut voluptas totam sit illum
        
        id: 14
        
        ### eveniet quod temporibus
        
        UserId: 2
        
        reprehenderit quos placeat velit minima officia dolores impedit repudiandae molestiae nam voluptas recusandae quis delectus officiis harum fugiat vitae
        
        id: 15
        
        ### sint suscipit perspiciatis velit dolorum rerum ipsa laboriosam odio
        
        UserId: 2
        
        suscipit nam nisi quo aperiam aut asperiores eos fugit maiores voluptatibus quia voluptatem quis ullam qui in alias quia est consequatur magni mollitia accusamus ea nisi voluptate dicta
        
        id: 16
        
        ### fugit voluptas sed molestias voluptatem provident
        
        UserId: 2
        
        eos voluptas et aut odit natus earum aspernatur fuga molestiae ullam deserunt ratione qui eos qui nihil ratione nemo velit ut aut id quo
        
        id: 17
        
        ### voluptate et itaque vero tempora molestiae
        
        UserId: 2
        
        eveniet quo quis laborum totam consequatur non dolor ut et est repudiandae est voluptatem vel debitis et magnam
        
        id: 18
        
        ### adipisci placeat illum aut reiciendis qui
        
        UserId: 2
        
        illum quis cupiditate provident sit magnam ea sed aut omnis veniam maiores ullam consequatur atque adipisci quo iste expedita sit quos voluptas
        
        id: 19
        
        ### doloribus ad provident suscipit at
        
        UserId: 2
        
        qui consequuntur ducimus possimus quisquam amet similique suscipit porro ipsam amet eos veritatis officiis exercitationem vel fugit aut necessitatibus totam omnis rerum consequatur expedita quidem cumque explicabo
        
        id: 20
        
        ### asperiores ea ipsam voluptatibus modi minima quia sint
        
        UserId: 3
        
        repellat aliquid praesentium dolorem quo sed totam minus non itaque nihil labore molestiae sunt dolor eveniet hic recusandae veniam tempora et tenetur expedita sunt
        
        id: 21
        
        ### dolor sint quo a velit explicabo quia nam
        
        UserId: 3
        
        eos qui et ipsum ipsam suscipit aut sed omnis non odio expedita earum mollitia molestiae aut atque rem suscipit nam impedit esse
        
        id: 22
        
        ### maxime id vitae nihil numquam
        
        UserId: 3
        
        veritatis unde neque eligendi quae quod architecto quo neque vitae est illo sit tempora doloremque fugit quod et et vel beatae sequi ullam sed tenetur perspiciatis
        
        id: 23
        
        ### autem hic labore sunt dolores incidunt
        
        UserId: 3
        
        enim et ex nulla omnis voluptas quia qui voluptatem consequatur numquam aliquam sunt totam recusandae id dignissimos aut sed asperiores deserunt
        
        id: 24
        
        ### rem alias distinctio quo quis
        
        UserId: 3
        
        ullam consequatur ut omnis quis sit vel consequuntur ipsa eligendi ipsum molestiae et omnis error nostrum molestiae illo tempore quia et distinctio
        
        id: 25
        
        ### est et quae odit qui non
        
        UserId: 3
        
        similique esse doloribus nihil accusamus omnis dolorem fuga consequuntur reprehenderit fugit recusandae temporibus perspiciatis cum ut laudantium omnis aut molestiae vel vero
        
        id: 26
        
        ### quasi id et eos tenetur aut quo autem
        
        UserId: 3
        
        eum sed dolores ipsam sint possimus debitis occaecati debitis qui qui et ut placeat enim earum aut odit facilis consequatur suscipit necessitatibus rerum sed inventore temporibus consequatur
        
        id: 27
        
        ### delectus ullam et corporis nulla voluptas sequi
        
        UserId: 3
        
        non et quaerat ex quae ad maiores maiores recusandae totam aut blanditiis mollitia quas illo ut voluptatibus voluptatem similique nostrum eum
        
        id: 28
        
        ### iusto eius quod necessitatibus culpa ea
        
        UserId: 3
        
        odit magnam ut saepe sed non qui tempora atque nihil accusamus illum doloribus illo dolor eligendi repudiandae odit magni similique sed cum maiores
        
        id: 29
        
        ### a quo magni similique perferendis
        
        UserId: 3
        
        alias dolor cumque impedit blanditiis non eveniet odio maxime blanditiis amet eius quis tempora quia autem rem a provident perspiciatis quia
        
        id: 30
        
        ### ullam ut quidem id aut vel consequuntur
        
        UserId: 4
        
        debitis eius sed quibusdam non quis consectetur vitae impedit ut qui consequatur sed aut in quidem sit nostrum et maiores adipisci atque quaerat voluptatem adipisci repudiandae
        
        id: 31
        
        ### doloremque illum aliquid sunt
        
        UserId: 4
        
        deserunt eos nobis asperiores et hic est debitis repellat molestiae optio nihil ratione ut eos beatae quibusdam distinctio maiores earum voluptates et aut adipisci ea maiores voluptas maxime
        
        id: 32
        
        ### qui explicabo molestiae dolorem
        
        UserId: 4
        
        rerum ut et numquam laborum odit est sit id qui sint in quasi tenetur tempore aperiam et quaerat qui in rerum officiis sequi cumque quod
        
        id: 33
        
        ### magnam ut rerum iure
        
        UserId: 4
        
        ea velit perferendis earum ut voluptatem voluptate itaque iusto totam pariatur in nemo voluptatem voluptatem autem magni tempora minima in est distinctio qui assumenda accusamus dignissimos officia nesciunt nobis
        
        id: 34
        
        ### id nihil consequatur molestias animi provident
        
        UserId: 4
        
        nisi error delectus possimus ut eligendi vitae placeat eos harum cupiditate facilis reprehenderit voluptatem beatae modi ducimus quo illum voluptas eligendi et nobis quia fugit
        
        id: 35
        
        ### fuga nam accusamus voluptas reiciendis itaque
        
        UserId: 4
        
        ad mollitia et omnis minus architecto odit voluptas doloremque maxime aut non ipsa qui alias veniam blanditiis culpa aut quia nihil cumque facere et occaecati qui aspernatur quia eaque ut aperiam inventore
        
        id: 36
        
        ### provident vel ut sit ratione est
        
        UserId: 4
        
        debitis et eaque non officia sed nesciunt pariatur vel voluptatem iste vero et ea numquam aut expedita ipsum nulla in voluptates omnis consequatur aut enim officiis in quam qui
        
        id: 37
        
        ### explicabo et eos deleniti nostrum ab id repellendus
        
        UserId: 4
        
        animi esse sit aut sit nesciunt assumenda eum voluptas quia voluptatibus provident quia necessitatibus ea rerum repudiandae quia voluptatem delectus fugit aut id quia ratione optio eos iusto veniam iure
        
        id: 38
        
        ### eos dolorem iste accusantium est eaque quam
        
        UserId: 4
        
        corporis rerum ducimus vel eum accusantium maxime aspernatur a porro possimus iste omnis est in deleniti asperiores fuga aut voluptas sapiente vel dolore minus voluptatem incidunt ex
        
        id: 39
        
        ### enim quo cumque
        
        UserId: 4
        
        ut voluptatum aliquid illo tenetur nemo sequi quo facilis ipsum rem optio mollitia quas voluptatem eum voluptas qui unde omnis voluptatem iure quasi maxime voluptas nam
        
        id: 40
        
        ### non est facere
        
        UserId: 5
        
        molestias id nostrum excepturi molestiae dolore omnis repellendus quaerat saepe consectetur iste quaerat tenetur asperiores accusamus ex ut nam quidem est ducimus sunt debitis saepe
        
        id: 41
        
        ### commodi ullam sint et excepturi error explicabo praesentium voluptas
        
        UserId: 5
        
        odio fugit voluptatum ducimus earum autem est incidunt voluptatem odit reiciendis aliquam sunt sequi nulla dolorem non facere repellendus voluptates quia ratione harum vitae ut
        
        id: 42
        
        ### eligendi iste nostrum consequuntur adipisci praesentium sit beatae perferendis
        
        UserId: 5
        
        similique fugit est illum et dolorum harum et voluptate eaque quidem exercitationem quos nam commodi possimus cum odio nihil nulla dolorum exercitationem magnam ex et a et distinctio debitis
        
        id: 43
        
        ### optio dolor molestias sit
        
        UserId: 5
        
        temporibus est consectetur dolore et libero debitis vel velit laboriosam quia ipsum quibusdam qui itaque fuga rem aut ea et iure quam sed maxime ut distinctio quae
        
        id: 44
        
        ### ut numquam possimus omnis eius suscipit laudantium iure
        
        UserId: 5
        
        est natus reiciendis nihil possimus aut provident ex et dolor repellat pariatur est nobis rerum repellendus dolorem autem
        
        id: 45
        
        ### aut quo modi neque nostrum ducimus
        
        UserId: 5
        
        voluptatem quisquam iste voluptatibus natus officiis facilis dolorem quis quas ipsam vel et voluptatum in aliquid
        
        id: 46
        
        ### quibusdam cumque rem aut deserunt
        
        UserId: 5
        
        voluptatem assumenda ut qui ut cupiditate aut impedit veniam occaecati nemo illum voluptatem laudantium molestiae beatae rerum ea iure soluta nostrum eligendi et voluptate
        
        id: 47
        
        ### ut voluptatem illum ea doloribus itaque eos
        
        UserId: 5
        
        voluptates quo voluptatem facilis iure occaecati vel assumenda rerum officia et illum perspiciatis ab deleniti laudantium repellat ad ut et autem reprehenderit
        
        id: 48
        
        ### laborum non sunt aut ut assumenda perspiciatis voluptas
        
        UserId: 5
        
        inventore ab sint natus fugit id nulla sequi architecto nihil quaerat eos tenetur in in eum veritatis non quibusdam officiis aspernatur cumque aut commodi aut
        
        id: 49
        
        ### repellendus qui recusandae incidunt voluptates tenetur qui omnis exercitationem
        
        UserId: 5
        
        error suscipit maxime adipisci consequuntur recusandae voluptas eligendi et est et voluptates quia distinctio ab amet quaerat molestiae et vitae adipisci impedit sequi nesciunt quis consectetur
        
        id: 50
        
        ### soluta aliquam aperiam consequatur illo quis voluptas
        
        UserId: 6
        
        sunt dolores aut doloribus dolore doloribus voluptates tempora et doloremque et quo cum asperiores sit consectetur dolorem
        
        id: 51
        
        ### qui enim et consequuntur quia animi quis voluptate quibusdam
        
        UserId: 6
        
        iusto est quibusdam fuga quas quaerat molestias a enim ut sit accusamus enim temporibus iusto accusantium provident architecto soluta esse reprehenderit qui laborum
        
        id: 52
        
        ### ut quo aut ducimus alias
        
        UserId: 6
        
        minima harum praesentium eum rerum illo dolore quasi exercitationem rerum nam porro quis neque quo consequatur minus dolor quidem veritatis sunt non explicabo similique
        
        id: 53
        
        ### sit asperiores ipsam eveniet odio non quia
        
        UserId: 6
        
        totam corporis dignissimos vitae dolorem ut occaecati accusamus ex velit deserunt et exercitationem vero incidunt corrupti mollitia
        
        id: 54
        
        ### sit vel voluptatem et non libero
        
        UserId: 6
        
        debitis excepturi ea perferendis harum libero optio eos accusamus cum fuga ut sapiente repudiandae et ut incidunt omnis molestiae nihil ut eum odit
        
        id: 55
        
        ### qui et at rerum necessitatibus
        
        UserId: 6
        
        aut est omnis dolores neque rerum quod ea rerum velit pariatur beatae excepturi et provident voluptas corrupti corporis harum reprehenderit dolores eligendi
        
        id: 56
        
        ### sed ab est est
        
        UserId: 6
        
        at pariatur consequuntur earum quidem quo est laudantium soluta voluptatem qui ullam et est et cum voluptas voluptatum repellat est
        
        id: 57
        
        ### voluptatum itaque dolores nisi et quasi
        
        UserId: 6
        
        veniam voluptatum quae adipisci id et id quia eos ad et dolorem aliquam quo nisi sunt eos impedit error ad similique veniam
        
        id: 58
        
        ### qui commodi dolor at maiores et quis id accusantium
        
        UserId: 6
        
        perspiciatis et quam ea autem temporibus non voluptatibus qui beatae a earum officia nesciunt dolores suscipit voluptas et animi doloribus cum rerum quas et magni et hic ut ut commodi expedita sunt
        
        id: 59
        
        ### consequatur placeat omnis quisquam quia reprehenderit fugit veritatis facere
        
        UserId: 6
        
        asperiores sunt ab assumenda cumque modi velit qui esse omnis voluptate et fuga perferendis voluptas illo ratione amet aut et omnis
        
        id: 60
        
        ### voluptatem doloribus consectetur est ut ducimus
        
        UserId: 7
        
        ab nemo optio odio delectus tenetur corporis similique nobis repellendus rerum omnis facilis vero blanditiis debitis in nesciunt doloribus dicta dolores magnam minus velit
        
        id: 61
        
        ### beatae enim quia vel
        
        UserId: 7
        
        enim aspernatur illo distinctio quae praesentium beatae alias amet delectus qui voluptate distinctio odit sint accusantium autem omnis quo molestiae omnis ea eveniet optio
        
        id: 62
        
        ### voluptas blanditiis repellendus animi ducimus error sapiente et suscipit
        
        UserId: 7
        
        enim adipisci aspernatur nemo numquam omnis facere dolorem dolor ex quis temporibus incidunt ab delectus culpa quo reprehenderit blanditiis asperiores accusantium ut quam in voluptatibus voluptas ipsam dicta
        
        id: 63
        
        ### et fugit quas eum in in aperiam quod
        
        UserId: 7
        
        id velit blanditiis eum ea voluptatem molestiae sint occaecati est eos perspiciatis incidunt a error provident eaque aut aut qui
        
        id: 64
        
        ### consequatur id enim sunt et et
        
        UserId: 7
        
        voluptatibus ex esse sint explicabo est aliquid cumque adipisci fuga repellat labore molestiae corrupti ex saepe at asperiores et perferendis natus id esse incidunt pariatur
        
        id: 65
        
        ### repudiandae ea animi iusto
        
        UserId: 7
        
        officia veritatis tenetur vero qui itaque sint non ratione sed et ut asperiores iusto eos molestiae nostrum veritatis quibusdam et nemo iusto saepe
        
        id: 66
        
        ### aliquid eos sed fuga est maxime repellendus
        
        UserId: 7
        
        reprehenderit id nostrum voluptas doloremque pariatur sint et accusantium quia quod aspernatur et fugiat amet non sapiente et consequatur necessitatibus molestiae
        
        id: 67
        
        ### odio quis facere architecto reiciendis optio
        
        UserId: 7
        
        magnam molestiae perferendis quisquam qui cum reiciendis quaerat animi amet hic inventore ea quia deleniti quidem saepe porro velit
        
        id: 68
        
        ### fugiat quod pariatur odit minima
        
        UserId: 7
        
        officiis error culpa consequatur modi asperiores et dolorum assumenda voluptas et vel qui aut vel rerum voluptatum quisquam perspiciatis quia rerum consequatur totam quas sequi commodi repudiandae asperiores et saepe a
        
        id: 69
        
        ### voluptatem laborum magni
        
        UserId: 7
        
        sunt repellendus quae est asperiores aut deleniti esse accusamus repellendus quia aut quia dolorem unde eum tempora esse dolore
        
        id: 70
        
        ### et iusto veniam et illum aut fuga
        
        UserId: 8
        
        occaecati a doloribus iste saepe consectetur placeat eum voluptate dolorem et qui quo quia voluptas rerum ut id enim velit est perferendis
        
        id: 71
        
        ### sint hic doloribus consequatur eos non id
        
        UserId: 8
        
        quam occaecati qui deleniti consectetur consequatur aut facere quas exercitationem aliquam hic voluptas neque id sunt ut aut accusamus sunt consectetur expedita inventore velit
        
        id: 72
        
        ### consequuntur deleniti eos quia temporibus ab aliquid at
        
        UserId: 8
        
        voluptatem cumque tenetur consequatur expedita ipsum nemo quia explicabo aut eum minima consequatur tempore cumque quae est et et in consequuntur voluptatem voluptates aut
        
        id: 73
        
        ### enim unde ratione doloribus quas enim ut sit sapiente
        
        UserId: 8
        
        odit qui et et necessitatibus sint veniam mollitia amet doloremque molestiae commodi similique magnam et quam blanditiis est itaque quo et tenetur ratione occaecati molestiae tempora
        
        id: 74
        
        ### dignissimos eum dolor ut enim et delectus in
        
        UserId: 8
        
        commodi non non omnis et voluptas sit autem aut nobis magnam et sapiente voluptatem et laborum repellat qui delectus facilis temporibus rerum amet et nemo voluptate expedita adipisci error dolorem
        
        id: 75
        
        ### doloremque officiis ad et non perferendis
        
        UserId: 8
        
        ut animi facere totam iusto tempore molestiae eum aut et dolorem aperiam quaerat recusandae totam odio
        
        id: 76
        
        ### necessitatibus quasi exercitationem odio
        
        UserId: 8
        
        modi ut in nulla repudiandae dolorum nostrum eos aut consequatur omnis ut incidunt est omnis iste et quam voluptates sapiente aliquam asperiores nobis amet corrupti repudiandae provident
        
        id: 77
        
        ### quam voluptatibus rerum veritatis
        
        UserId: 8
        
        nobis facilis odit tempore cupiditate quia assumenda doloribus rerum qui ea illum et qui totam aut veniam repellendus
        
        id: 78
        
        ### pariatur consequatur quia magnam autem omnis non amet
        
        UserId: 8
        
        libero accusantium et et facere incidunt sit dolorem non excepturi qui quia sed laudantium quisquam molestiae ducimus est officiis esse molestiae iste et quos
        
        id: 79
        
        ### labore in ex et explicabo corporis aut quas
        
        UserId: 8
        
        ex quod dolorem ea eum iure qui provident amet quia qui facere excepturi et repudiandae asperiores molestias provident minus incidunt vero fugit rerum sint sunt excepturi provident
        
        id: 80
        
        ### tempora rem veritatis voluptas quo dolores vero
        
        UserId: 9
        
        facere qui nesciunt est voluptatum voluptatem nisi sequi eligendi necessitatibus ea at rerum itaque harum non ratione velit laboriosam quis consequuntur ex officiis minima doloremque voluptas ut aut
        
        id: 81
        
        ### laudantium voluptate suscipit sunt enim enim
        
        UserId: 9
        
        ut libero sit aut totam inventore sunt porro sint qui sunt molestiae consequatur cupiditate qui iste ducimus adipisci dolor enim assumenda soluta laboriosam amet iste delectus hic
        
        id: 82
        
        ### odit et voluptates doloribus alias odio et
        
        UserId: 9
        
        est molestiae facilis quis tempora numquam nihil qui voluptate sapiente consequatur est qui necessitatibus autem aut ipsa aperiam modi dolore numquam reprehenderit eius rem quibusdam
        
        id: 83
        
        ### optio ipsam molestias necessitatibus occaecati facilis veritatis dolores aut
        
        UserId: 9
        
        sint molestiae magni a et quos eaque et quasi ut rerum debitis similique veniam recusandae dignissimos dolor incidunt consequatur odio
        
        id: 84
        
        ### dolore veritatis porro provident adipisci blanditiis et sunt
        
        UserId: 9
        
        similique sed nisi voluptas iusto omnis mollitia et quo assumenda suscipit officia magnam sint sed tempora enim provident pariatur praesentium atque animi amet ratione
        
        id: 85
        
        ### placeat quia et porro iste
        
        UserId: 9
        
        quasi excepturi consequatur iste autem temporibus sed molestiae beatae et quaerat et esse ut voluptatem occaecati et vel explicabo autem asperiores pariatur deserunt optio
        
        id: 86
        
        ### nostrum quis quasi placeat
        
        UserId: 9
        
        eos et molestiae nesciunt ut a dolores perspiciatis repellendus repellat aliquid magnam sint rem ipsum est
        
        id: 87
        
        ### sapiente omnis fugit eos
        
        UserId: 9
        
        consequatur omnis est praesentium ducimus non iste neque hic deserunt voluptatibus veniam cum et rerum sed
        
        id: 88
        
        ### sint soluta et vel magnam aut ut sed qui
        
        UserId: 9
        
        repellat aut aperiam totam temporibus autem et architecto magnam ut consequatur qui cupiditate rerum quia soluta dignissimos nihil iure tempore quas est
        
        id: 89
        
        ### ad iusto omnis odit dolor voluptatibus
        
        UserId: 9
        
        minus omnis soluta quia qui sed adipisci voluptates illum ipsam voluptatem eligendi officia ut in eos soluta similique molestias praesentium blanditiis
        
        id: 90
        
        ### aut amet sed
        
        UserId: 10
        
        libero voluptate eveniet aperiam sed sunt placeat suscipit molestias similique fugit nam natus expedita consequatur consequatur dolores quia eos et placeat
        
        id: 91
        
        ### ratione ex tenetur perferendis
        
        UserId: 10
        
        aut et excepturi dicta laudantium sint rerum nihil laudantium et at a neque minima officia et similique libero et commodi voluptate qui
        
        id: 92
        
        ### beatae soluta recusandae
        
        UserId: 10
        
        dolorem quibusdam ducimus consequuntur dicta aut quo laboriosam voluptatem quis enim recusandae ut sed sunt nostrum est odit totam sit error sed sunt eveniet provident qui nulla
        
        id: 93
        
        ### qui qui voluptates illo iste minima
        
        UserId: 10
        
        aspernatur expedita soluta quo ab ut similique expedita dolores amet sed temporibus distinctio magnam saepe deleniti omnis facilis nam ipsum natus sint similique omnis
        
        id: 94
        
        ### id minus libero illum nam ad officiis
        
        UserId: 10
        
        earum voluptatem facere provident blanditiis velit laboriosam pariatur accusamus odio saepe cumque dolor qui a dicta ab doloribus consequatur omnis corporis cupiditate eaque assumenda ad nesciunt
        
        id: 95
        
        ### quaerat velit veniam amet cupiditate aut numquam ut sequi
        
        UserId: 10
        
        in non odio excepturi sint eum labore voluptates vitae quia qui et inventore itaque rerum veniam non exercitationem delectus aut
        
        id: 96
        
        ### quas fugiat ut perspiciatis vero provident
        
        UserId: 10
        
        eum non blanditiis soluta porro quibusdam voluptas vel voluptatem qui placeat dolores qui velit aut vel inventore aut cumque culpa explicabo aliquid at perspiciatis est et voluptatem dignissimos dolor itaque sit nam
        
        id: 97
        
        ### laboriosam dolor voluptates
        
        UserId: 10
        
        doloremque ex facilis sit sint culpa soluta assumenda eligendi non ut eius sequi ducimus vel quasi veritatis est dolores
        
        id: 98
        
        ### temporibus sit alias delectus eligendi possimus magni
        
        UserId: 10
        
        quo deleniti praesentium dicta non quod aut est molestias molestias et officia quis nihil itaque dolorem quia
        
        id: 99
        
        ### at nam consequatur ea labore ea harum
        
        UserId: 10
        
        cupiditate quo est a modi nesciunt soluta ipsa voluptas error itaque dicta in autem qui minus magnam et distinctio eum accusamus ratione error aut
        
        id: 100
        
    

* * *

### Property accessor using `'::'`

You can access data using the property accessor `'::'` from a or file, api as into a component.

Assume the data in a `json` file or an api has the following representation:

    {"Leanne Graham":{
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
            ...
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
            ...
    }
    }, "Ervin Howell": {
    "id": 2,
    "name": "Ervin Howell",
    "username": "Antonette",
    "email": "Shanna@melissa.tv",
    "address": {
            ...
        },
    "phone": "010-692-6593 x09125",
    "website": "anastasia.net",
    "company": {
        ...
        }
    }}
  

You can access a record like this:

    `<vt_user vt:from-file="file.json::Leanne Graham" />`
    
  

or in the case of api:

    `<vt_user vt:from-api="https://jsonplaceholder.typicode.com/users::Leanne Graham" />`
    
  

As shown above, the `'::'` accessor \`accesses\` a record, kind of how a key is used in a json dictionary/javascript object/hash-map.

`**NOTE**`The value must accessed by the prop accessor **MUST** be a `dictionary` or a `list of dictionaries.`

If the value of the `key` is a list, you then must use `vt:map-from-[list|api]`.

e.g

    `<vt_users vt:map-from-file="file.json::users" />`
    
  

    `<vt_users vt:map-from-api="https://myapi.com::users" />`
    
  

**`**NOTE**` The prop accessor only goes to one level, so the json structure matters (a multilevel prop accessor is in development).**

i.e

If you have json data in the following format:

    `{       "Ervin Howell":         {           "id": 2,           "name": "Ervin Howell",           "username": "Antonette",           "email": "Shanna@melissa.tv",           "address": {                   ...               },           "phone": "010-692-6593 x09125",           "website": "anastasia.net",           "company": {               ...               }         }     }`
    
  

If you access the record (whether from an api or file), the data is injected as is, meaning, the accessor isnt able to reach the values for `"address"` and `"company"`.

* * *

Other cool `vt` features:
-------------------------

### In Place components

Another cool vt feature is in-place components, which are templates which are defined inplace and consumed directly without having to import them.

    `<div vt:from-api='https://myapi.json::user' class="card m-2">             <div class="card-header">                 <h3>{title}</h3>             </div>             <div class="card-body">                 <div>UserId: {userid}</div>                 <p>{body}</p>             </div>             <div class="card-footer">                 <small>id: {id}</small>             </div>         </div>`
    
  

In this example, the data accessed is a dictionary that will directly be injected into the template.

`**NOTE**`This feature currently works for `vt:from, vt:from-file and vt:from-api` only, which means the data to be injected into the template can only be a dictionary.,

* * *

### Special `vt` attributes and tags:

1.  #### `vt:parent`
    
    *   `vt:parent` is a special attribute used when you want to re-use a base/parent component.
        
        This comes in handy, when you want to re-use a `parent` html component for different pages
        
        Assume you have a `Base.html` like the one below:
        
                `<!DOCTYPE html>             <html             lang="en"             vt_imports="['components/scripts.html','components/vt_header.html' ]"             >             <head>                 <meta charset="UTF-8" />                 <meta name="viewport" content="width=device-width, initial-scale=1.0" />                 <link rel="shortcut icon" href="/images/logo_bg.jpg" />                 <link rel="stylesheet" href="style.css" type="text/css" />                 <title>Vanilla Templates | {page}</title>             </head>             <body>                 <div class="container">                 <vt_header title="Vanilla Templates" version="1.0.0" />                 <vt_child />                 </div>             </body>             <scripts />             </html>`
                
              
        
        This is a sample component that inherits the `Base.html`:
        
                `<vt_frag vt:parent="components/Base.html" page="Home">                 <div                     style="min-height: 400px"                     class="container d-flex align-items-center justify-content-center flex-column gap-4"                 >                     <p>Welcome to <code>vanilla templates</code></p>                     <img style="width: 120px" src="images/logo_bg.jpg" />                     <ul>                     <li>                         <a href="/docs.html">Go to docs 📃</a>                     </li>                     <li>                         <a href="#">Buy me a coffee ☕</a>                     </li>                     </ul>                 </div>             </vt_frag>`
        
                
              
        
        Few things to take note of:
        
        *   The parent components can have placeholders like a regular template, which are passed from the child components.
            
            e.g the `page` prop in the above example defined in the base html should be passed by every child that inherits.
            
        *   In the parent template, there is a `vt_child` special component, which is replaced by any child that inherits this parent.
            
            `code>NOTE`As highlighted in the Base.html, the `vt__child` is not imported and is a **reserved** name.
            
        *   In the child component that is inheriting the parent, you **MUST** declare the `vt:parent` then pass the path of the parent component.
        *   The `vt_frag` is going to be discussed in the next section.
    
2.  #### `vt_frag`
    
    By now, you have seen the `<vt_frag></vt_frag>` in the various examples shown above.
    
    The `vt_frag` (**vt fragment in full**)is a special tag in `Vanilla Templates` used when you want to wrap a group of tags but you don't the tag you wrap with to end up in the final build.
    
    In short, when `vt` is building your site, and it comes across this tag, it **'unwraps'** and renders it's children.
    

* * *

### Static Site Generation

`Vanilla Templates` has a build command: `python3 -m vt.build` which compiles all the different components and after filling them the appropriate data.

The final html file and the contents in the `public` folder are dumped in the `__vt_build__` in the root of your project.

From here you can deploy it as is, as it is a basic html file.

It is worth noting that with `Vanilla Templates`, you can build a significantly bigger website with multiple pages re-using the same templates, and use your favourite library to add some interactivity, a.k.a make it `reactive` (a good recommendation would be [htmx](https://htmx.org/docs/)).

* * *

### Server Side Rendering

Vanilla Templates uses a `Flask` server activated by `python3 -m vt.serve` for developement and debugging.

For the most part, Vanilla Templates SSR compiles the components and renders the website without added backend features like database data injection.

This leads to the fact that most Server Side Features are still largely in development 😢, but we hope the features above suffice enough to bootstrap your 'Javascript-frameworkless'😂 web developemnt.

* * *

[❤ Support vt](https://www.buymeacoffee.com/fredrickkyeki)

© Vanilla Templates document.write(new Date().getFullYear());

Author: [Fred](https://github.com/FREDRICKKYEKI  )
