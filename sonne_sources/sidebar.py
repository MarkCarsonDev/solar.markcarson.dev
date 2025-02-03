sidebar_html = '<nav id="sidebar">\
            <ul>\
                <a href="#"><li id="kp1" class="keypress">Home</li></a>\
                <a href="#about"><li id="kp2" class="keypress">About</li></a>\
                <a href="#projects"><li id="kp3" class="keypress">Projects</li></a>\
                <a href="#education"><li id="kp4" class="keypress">Education</li></a>\
                <li class="listsep"></li>\
                <a href="/blog"><li id="kpB" class="keypress">Blog</li></a>\
                <a href="#contact"><li id="kpC" class="keypress">Contact</li></a>\
\
            </ul>\
        </nav>'

sidebar_blog_html = '<nav id="sidebar">\
            <ul>\
                <a href="/blog"><li id="kpM" class="keypress">Main Page</li></a>\
                <a href="#contact"><li id="kpC" class="keypress">Contact</li></a>\
\
            </ul>\
        </nav>'

sonne_var("sidebar", sidebar_html)
sonne_var("sidebar_blog", sidebar_blog_html)