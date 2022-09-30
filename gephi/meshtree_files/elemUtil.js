function appendClass(name) {

    function append(elems) {

        if (Array.isArray(elems))
            return elems.map(append);

        else {

            if (typeof elems == "string")
                elems = document.getElementById(elems);

            const { className } = elems,
                    classes     = splitClasses(className);

            if (classes.indexOf(name) == -1)
                elems.className =
                    classes.length ? `${className} ${name}` : name;

            return elems;

        }

    }

    return append;

}

function removeClass(name) {

    function remove(elems) {
        if (Array.isArray(elems))
            return elems.map(remove);
        else {
            if (typeof elems == "string")
                elems = document.getElementById(elems);
            elems.className = splitClasses(elems.className)
                 .filter(type => type != name).join(" ");
            return elems;
        }
    }

    return remove;

}

function splitClasses(classes) {
    return classes ? classes.trim().split(/ +/) : [];
}

function displayElem(elem, display) {
    if (typeof elem == "string") elem = document.getElementById(elem);
    if (       elem            ) elem.style.display = display;
    return elem;
}

const showElem = (elem, display) => displayElem(elem, display || "block"),
      hideElem =  elem           => displayElem(elem, "none"            );

function toggleCollapse(target, trigger, display) {
    target = document.getElementById(target);
    if (target.style.display == "none") showCollapse(target, trigger, display);
    else                                hideCollapse(target, trigger         );
}

const appendCollapsed = appendClass("collapsed"),
      removeCollapsed = removeClass("collapsed"),
      appendIn        = appendClass("in"       ),
      removeIn        = removeClass("in"       );

function showCollapse(target, trigger, display) {
    appendIn       (showElem(target, display)).ariaExpanded = "true";
    removeCollapsed(trigger || this          ).ariaExpanded = "true";
}

function hideCollapse(target, trigger) {
    removeIn       (hideElem(target)).ariaExpanded = "false";
    appendCollapsed(trigger || this ).ariaExpanded = "false";
}
