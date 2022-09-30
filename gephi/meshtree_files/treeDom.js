var treeDcms = dcmsParam("?");

function openTree(button) {

    var listItem = button.parentNode;

    if (listItem.getElementsByTagName("ul").length) {
        displayTree(listItem, "block", 0, 1);
        return;
    }

    var childReq = new XMLHttpRequest();

    childReq.addEventListener("load", function () {
        listItem.innerHTML += this.responseText;
        displayTree(listItem, "block", 0, 1);
    });

    var itemId = listItem.getElementsByTagName("a").item(0).id;
    childReq.open("GET",
                  "/api/tree/"
                  + itemId.substring(itemId.lastIndexOf("_node_") + 6)
                    .replace(/_/g, ".")
                  + treeDcms);
    childReq.send();

}

function closeTree(button) { displayTree(button.parentNode, "none", 1, 0); }

function displayTree(listItem, display, button, sibling) {

    listItem.getElementsByTagName("ul").item(0).style.display = display;

    var buttons = listItem.getElementsByTagName("i");
    buttons.item(button ).style.display = "none";
    buttons.item(sibling).style.display = "inline";

}
