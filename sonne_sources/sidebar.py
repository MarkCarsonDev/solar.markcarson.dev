sidebar_html = '<nav id="sidebar">\
            <ul>\
                <a href="#"><li id="kp1" class="keypress"><span>Home</span></li></a>\
                <a href="#about"><li id="kp2" class="keypress"><span>About</span></li></a>\
                <a href="#projects"><li id="kp3" class="keypress"><span>Projects</span></li></a>\
                <a href="#education"><li id="kp4" class="keypress"><span>Education</span></li></a>\
                <li class="listsep"></li>\
                <a href="/blog"><li id="kpB" class="keypress"><span>Blog</span></li></a>\
                <a href="/contact"><li id="kpC" class="keypress"><span>Contact</span></li></a>\
\
            </ul>\
        </nav>'

sidebar_blog_html = '<nav id="sidebar">\
            <ul>\
                <a href="/"><li id="kpH" class="keypress"><span>Home</span></li></a>\
                <a href="/contact"><li id="kpC" class="keypress"><span>Contact</span></li></a>\
\
            </ul>\
        </nav>'

sonne_var("sidebar", sidebar_html)
sonne_var("sidebar_blog", sidebar_blog_html)