window.onload = function () {
    change_delete_to_replace()
};

function change_delete_to_replace(){
    let div_elem;
    let replace_before_elem;
    let replace_after_elem;
    let delete_string_elem;
    let label;
    let btn;

    div_elem = document.getElementById('js-tab');
    div_elem.classList.add('bg-gray-200');
    div_elem.classList.remove('bg-gray-300');

    replace_before_elem = document.getElementById('js-replace-before');
    label = replace_before_elem.previousElementSibling
    replace_before_elem.classList.remove('hidden');
    label.classList.remove('hidden');

    replace_after_elem = document.getElementById('js-replace-after');
    label = replace_after_elem.previousElementSibling
    replace_after_elem.classList.remove('hidden');
    label.classList.remove('hidden');

    delete_string_elem = document.getElementById('js-delete-string');
    label = delete_string_elem.previousElementSibling
    delete_string_elem.classList.add('hidden');
    label.classList.add('hidden');

    btn = document.getElementById('js-push-btn');
    btn.setAttribute("onclick", "push_replaces()");
}

function change_replace_to_delete(){
    let div_elem;
    let replace_before_elem;
    let replace_after_elem;
    let delete_string_elem;
    let label;
    let btn;

    div_elem = document.getElementById('js-tab');
    div_elem.classList.add('bg-gray-300');
    div_elem.classList.remove('bg-gray-200');

    replace_before_elem = document.getElementById('js-replace-before');
    label = replace_before_elem.previousElementSibling
    replace_before_elem.classList.add('hidden');
    label.classList.add('hidden');

    replace_after_elem = document.getElementById('js-replace-after');
    label = replace_after_elem.previousElementSibling
    replace_after_elem.classList.add('hidden');
    label.classList.add('hidden');

    delete_string_elem = document.getElementById('js-delete-string');
    label = delete_string_elem.previousElementSibling
    delete_string_elem.classList.remove('hidden');
    label.classList.remove('hidden');

    btn = document.getElementById('js-push-btn');
    btn.setAttribute("onclick", "push_deletes()");
}





function get_delete_button(){
    let delete_btn = document.createElement("button");
    delete_btn.appendChild(document.createTextNode("取り消し"));
    delete_btn.setAttribute("class", "text-red-300 pl-4 cursor-pointer");
    delete_btn.setAttribute("onclick", "delete_me(this)");
    return delete_btn;
}

function make_replace_input(col_name, before_str, after_str){
    let div_elem = document.createElement("div");
    div_elem.setAttribute("class", "border-t border-gray-300 my-2");

    let col = document.createElement("input");
    col.setAttribute("type", "hidden");
    col.setAttribute("name", "replaces_col_name");
    col.setAttribute("value", col_name);

    let before = document.createElement("input");
    before.setAttribute("type", "hidden");
    before.setAttribute("name", "replaces_before");
    before.setAttribute("value", before_str);

    let after = document.createElement("input");
    after.setAttribute("type", "hidden");
    after.setAttribute("name", "replaces_after");
    after.setAttribute("value", after_str);

    str_elem = document.createTextNode(col_name + ' の ' +before_str + " を " + after_str + "に変換");

    div_elem.appendChild(col);
    div_elem.appendChild(before);
    div_elem.appendChild(after);
    div_elem.appendChild(str_elem);
    return div_elem;
}

function push_replaces(){
    let col_name = document.getElementById('js-column').value
    let before_str = document.getElementById('js-replace-before').value
    let after_str = document.getElementById('js-replace-after').value

    parent_div_elem = document.getElementById("js-replace-form");
    let div_elem = make_replace_input(col_name, before_str, after_str);
    div_elem.appendChild(get_delete_button());
    parent_div_elem.appendChild(div_elem);
}


function make_delete_input( col_name, delete_str,) {
    let div_elem = document.createElement("div");
    div_elem.setAttribute("class", "border-t border-gray-300 my-2");

    let col = document.createElement("input");
    col.setAttribute("type", "hidden");
    col.setAttribute("name", "deletes_col_name");
    col.setAttribute("value", col_name);

    let delete_elem = document.createElement("input");
    delete_elem.setAttribute("type", "hidden");
    delete_elem.setAttribute("name", "deletes_str");
    delete_elem.setAttribute("value", delete_str);

    str_elem = document.createTextNode(col_name + ' の ' + delete_str + " を削除");

    div_elem.appendChild(col);
    div_elem.appendChild(delete_elem);
    div_elem.appendChild(str_elem);
    return div_elem;
}


function push_deletes() {
    let col_name = document.getElementById('js-column').value
    let delete_str = document.getElementById('js-delete-string').value

    parent_div_elem = document.getElementById("js-replace-form");
    let div_elem = make_delete_input(col_name, delete_str);
    div_elem.appendChild(get_delete_button());
    parent_div_elem.appendChild(div_elem);

}

function delete_me(elem){
    let parent = elem.parentNode;
    parent.remove();
}