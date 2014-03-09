============
Data As Code
============
:date: 2014-03-08
:category: programming
:tags: data, code
:author: Yusuke Tsutsumi


I followed through the exercises of `Seven Languages in Seven Weeks
<http://pragprog.com/book/btlang/seven-languages-in-seven-weeks>`_ a
while back, and there was a really interesting concept introduced by
clojure (which really extends it's idea from lisp): that code is data
and data is code. The idea that a programming language's syntax is
flexible enough where a description of the data is actually code itself.

A good example of where this sort of binding works well is with
configuration and data files: These files are almost always authored
in a intermediary markup format that is then parsed and interpreted by
a programming language of choice. For a language where code is data,
the data or configuration file is just another file with code, and it
just has to be loaded and parsed to be understood by a program.

I didn't consider the strength in such an idea at first. In fact, I
dismissed it as a nice-to-have, a concept whose absence in a language
was a mild detriment, but not one that would really hamper a
developers ability to do what they need to.

But the more I thought about it, the more my opinion changed. With
every new config file I faced, my opinion changed all the more.


For an example, let's take the approach of data-as-code with a
language where the design wasn't designed that way. Java has a lot of strengths, but
It has it's weaknesses. Let's say I want to express a menu. In code directly, that looks like::


    FileMenu menu = new FileMenu(
      new Tab[] {
        new Tab("File",
          new Command[] {
            new Command("New"),
            new Command("Open"),
            new Command("Save"),
            new Command("Save As...")
          })
      }
    );


Now in lisp(-ish)::

  (filemenu
    (tabs
      (tab "File" (
            (command "New")
            (command "Open")
            (command "Save")
            (command "Save as...")))))

It's so clean! It actually looks like a config file at this point: a
data format such as json or yaml probably wouldn't make this any more
readable. Even Python, which is a bit more dynamic that Java, doesn't
look as clean::

  menu = FileMenu(
    tabs(
      tab("File", (
        command("New"),
        command("Open"),
        command("Save"),
        command("Save as...")
      ))
    ))
  )

There's something about those parentheses. So for these languages
where the code-data bind is not as strong, separate data is
represented as a completely separate format, either something abstract
like a map or a separate data file. However, this creates a separation
of implementation and representation. This adds any of the additional
functional overheads:

* a deserializer, turning data -> in programming language representation
* a validator, ensuring that the data is valid
* a serializer, turning programming language representation -> data

When your data is already represented as code, you remove these
additional layers of abstraction: your interpreter/compiler will
figure out validity for you! Not only that, but your code
representation is just as clean, so it's just like interacting with
your data directly. In fact, that's precisely what you're doing.

The insane thing is, as your code becomes more powerful, your data
does as well. Parsing the code directly allows you to add complex
configuration with ease. For example, adding a conditional statement
in the filemenu in lisp above is::

  (filemenu
    (tabs
      (tab "File" (
            (command "New")
            (command "Open")
            (command "Save")
            (if (isOSX)
              (command "Save to icloud")
            )
            (command "Save as...")))))

Now imagine how you would implement a check like that in an xml or
json file. I was able to take advantage of a new method (isOSX)
immediately, as well as built-in methods like an if statement.
Because data is code, your representation is just as powerful as your
language. Now that is power at the touch of your fingertips.

Lisp and it's cousins are definitely weird to get used to, but the true
power of the direct binding of code and data that is built in is a
concept worth really exploring and understanding. I'm just diving in
and already having a blast.
