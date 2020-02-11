document.getElementById("overview_img").src=overview_uri;
document.getElementById("use_case_diagram").src=use_case_uri;
document.getElementById("homepage").src=homepage_uri;
document.getElementById("login").src=login_uri;
document.getElementById("teachers_landing").src=teachers_landing_uri;
document.getElementById("teachers_upload").src=teachers_load_files_uri;
document.getElementById("teachers_view_stats").src=teachers_view_stats_uri;
document.getElementById("student_landing").src=student_landing_uri;
document.getElementById("student_view_doc").src=student_view_class_doc_uri;
document.getElementById("student_opened_doc").src=student_opened_doc_uri;



// Global variables
var doc = new jsPDF()
var whole = document.querySelector("#html-2-pdfwrapper");
var y_pos;

function frontPage(){
    var front_page = whole.querySelector(".main #front_page");

    y_pos = 30;
    doc.setFontSize(30)
    doc.text(20, 30, front_page.querySelector("#p1").textContent);
    y_pos += 20;

    doc.setFontSize(20);
    doc.text(20, y_pos, front_page.querySelector("#p2").textContent);
    y_pos += 20;

    doc.setFontSize(30);
    doc.text(20, y_pos, front_page.querySelector("#p3").textContent);
    y_pos += 20;

    doc.setFontSize(20);
    doc.text(20, y_pos, front_page.querySelector("#p4").textContent);
    y_pos += 20;

    doc.setFontSize(20);
    doc.text(20, y_pos, front_page.querySelector("#p5").textContent);
    y_pos += 20;

    doc.setFontSize(20);
    doc.text(20, y_pos, front_page.querySelector("#p6").textContent);
    y_pos += 20;

    doc.autoTable({ html: '#p7', margin: { top: y_pos-10 } })
    y_pos += 50;

    doc.setFontSize(13);
    doc.text(20, y_pos, front_page.querySelector("#p8").textContent + " Dr Nabeel Mohammed (NbM)");
    y_pos += 10;

    doc.text(20, y_pos, front_page.querySelector("#p9").textContent + " CSE327");
    y_pos += 10;

    doc.text(20, y_pos, front_page.querySelector("#p10").textContent + " 1");
    y_pos += 10;

    doc.text(20, y_pos, front_page.querySelector("#p11").textContent + " 04/02/2020");
    y_pos += 10;
    //doc.addImage(imgData, 'JPEG', 15, 40, 180, 160)
}
function table_of_contents(){
    doc.addPage();
    y_pos = 30;

    var toc_page = whole.querySelector("#div_toc");

    doc.setFontSize(30);
    doc.text(20, y_pos, toc_page.querySelector("#table_of_contents").textContent);
    y_pos += 20;

    var rows = toc_page.querySelectorAll("ol");
    for(i = 0; i < rows.length; ++i){
        doc.setFontSize(12);
        doc.text(-10, y_pos, rows[i].textContent);
        var Height = rows[i].offsetHeight;
        y_pos += Height;
        if(y_pos >= 500){
            break;
        }
    }
}
function introduction(){
    doc.addPage();
    var cur_div = whole.querySelector("#intro_page");

    y_pos = 30;
    var rows = cur_div.querySelectorAll("*");
    for(i = 0; i < rows.length; ++i){
        if(rows[i].tagName === "H1"){
            doc.setFontSize(22);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 15;
        }
        else if(rows[i].tagName === "H2"){
            doc.setFontSize(15);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 10;
        }
        else if(rows[i].tagName === "P"){
            doc.setFontSize(12);
            var para = rows[i].textContent.split(" ");
            var para_with_break = "";
            var cur_len = 0;
            var num_lines = 0;
            for(k = 0; k < para.length; ++k){
                cur_len += para[k].length;
                if(cur_len >= 70){
                    para_with_break += "\n";
                    cur_len = 0;
                    ++num_lines;
                }
                para_with_break += para[k] + " ";
            }
            doc.text(20, y_pos, para_with_break);
            y_pos += 10 + 8 * num_lines;
        }
        if(i < rows.length-1 && rows[i+1].id === "one.five"){
            y_pos = 30;
            doc.addPage();
        }
    }
}
function overall_description(){
    var cur_div = whole.querySelector("#overall_desc");
    // continuing from last insertion (y_pos unchanged)

    var rows = cur_div.querySelectorAll("*");
    for(i = 0; i < rows.length; ++i){
        if(rows[i].tagName === "H1"){
            doc.setFontSize(22);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 15;
        }
        else if(rows[i].tagName === "H2"){
            doc.setFontSize(15);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 10;
        }
        else if(rows[i].tagName === "P"){
            doc.setFontSize(12);
            var para = rows[i].textContent.split(" ");
            var para_with_break = "";
            var cur_len = 0;
            var num_lines = 0;
            for(k = 0; k < para.length; ++k){
                cur_len += para[k].length;
                if(cur_len >= 70){
                    para_with_break += "\n";
                    cur_len = 0;
                    ++num_lines;
                }
                para_with_break += para[k] + " ";
            }
            doc.text(20, y_pos, para_with_break);
            y_pos += 5 + 8 * num_lines;
        }
        else if(rows[i].tagName === "OL"){
            doc.setFontSize(12);
            var items = rows[i].querySelectorAll("li");
            for(j = 0; j < items.length; ++j){
                var words = items[j].textContent.split(" ");
                var cur_line = "";
                var num_lines = 1;
                var cur_len = 0;
                for(k = 0; k < words.length; ++k){
                    cur_len += words[k].length;
                    if(cur_len >=  70){
                        cur_len = 0;
                        cur_line += "\n";
                        ++num_lines;
                    }
                    cur_line += words[k] + " ";

                }
                doc.text(20, y_pos, cur_line);
                y_pos += num_lines * 10;
            }
        }
        else if(rows[i].tagName === "IMG"){
            doc.addImage(rows[i].src, 'JPEG', 35, y_pos-10, 100, 110);
            y_pos += 110;
            doc.text(20+20, y_pos, "Figure 1.1: Product Overview");
            y_pos = 30;
            doc.addPage();
        }
    }
}

function specific_requirements(){
    var cur_div = whole.querySelector("#spec_reqs");
    doc.addPage();
    y_pos = 30;

    var rows = cur_div.querySelectorAll("*");
    for(i = 0; i < rows.length; ++i){
        if(rows[i].id === "add_new_page"){
            doc.addPage();
            y_pos = 30;
        }
        if(rows[i].tagName === "H1"){
            doc.setFontSize(25);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 15;
        }
        else if(rows[i].tagName === "H2"){
            if(rows[i].id == "three.two" || rows[i].id == "three.three"){
                doc.addPage();
                y_pos = 30;
            }
            doc.setFontSize(20);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 10;
        }
        else if(rows[i].tagName === "H3"){
            if(rows[i].id === "three.three.two"){
                doc.addPage();
                y_pos = 30;
            }
            y_pos += 10;
            doc.setFontSize(17);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 8;
        }
        else if(rows[i].tagName === "H4"){
            y_pos += 5;
            doc.setFontSize(14);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 10;
        }
        else if(rows[i].tagName === "H5"){
            doc.setFontSize(13);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 5;
        }
        else if(rows[i].tagName === "P"){
            doc.setFontSize(12);
            var para = rows[i].textContent.split(" ");
            var para_with_break = "";
            var cur_len = 0;
            var num_lines = 0;
            for(k = 0; k < para.length; ++k){
                cur_len += para[k].length;
                if(cur_len >= 70){
                    para_with_break += "\n";
                    cur_len = 0;
                    ++num_lines;
                }
                para_with_break += para[k] + " ";
            }
            if(rows[i].id === "flow_of_events"){
                y_pos += 5;
            }
            doc.text(20, y_pos, para_with_break);
            y_pos += 5 + 8 * num_lines;
        }
        else if(rows[i].tagName === "OL" || rows[i].tagName === "UL"){
            doc.setFontSize(12);
            var items = rows[i].querySelectorAll("li");
            if(items.length === 0 || !items){
                throw "items array is null";
            }
            for(j = 0; j < items.length; ++j){
                var words = items[j].textContent.split(" ");
                var cur_line = "";
                var num_lines = 1;
                var cur_len = 0;
                for(k = 0; k < words.length; ++k){
                    cur_len += words[k].length;
                    if(cur_len >=  70){
                        cur_len = 0;
                        cur_line += "\n";
                        ++num_lines;
                    }
                    cur_line += words[k] + " ";

                }
                doc.text(20, y_pos, cur_line);
                y_pos += num_lines * 7;
            }
        }
        else if(rows[i].tagName === "FIGURE"){
            var imgSource = rows[i].querySelector("img").src;
            var imgId = rows[i].querySelector("img").id;
            var caption = rows[i].querySelector("figcaption").textContent;
            if(imgId === "use_case_diagram"){
                if(y_pos + 155 >= 350){
                    doc.addPage();
                    y_pos = 30;
                }
                doc.addImage(imgSource, 'JPEG', 20, y_pos, 120, 150);
                y_pos += 155;
            }
            else {
                if(y_pos + 105 >= 350){
                    doc.addPage();
                    y_pos = 30;
                }
                doc.addImage(imgSource, 'JPEG', 20, y_pos, 80, 100);
                y_pos += 95;
            }
            doc.text(10+20, y_pos, caption);
            y_pos += 20;
        }
    }
}

function non_functional_req(){
    var cur_div = whole.querySelector("#other_non_func");

    var rows = cur_div.querySelectorAll("*");
    for(i = 0; i < rows.length; ++i){
        if(rows[i].tagName === "H1"){
            doc.setFontSize(22);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 15;
        }
        else if(rows[i].tagName === "H2"){
            if(rows[i].id === "four.three"){
                doc.addPage();
                y_pos = 30;
            }
            doc.setFontSize(15);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 10;
        }
        else if(rows[i].tagName === "P"){
            doc.setFontSize(12);
            var para = rows[i].textContent.split(" ");
            var para_with_break = "";
            var cur_len = 0;
            var num_lines = 0;
            for(k = 0; k < para.length; ++k){
                cur_len += para[k].length;
                if(cur_len >= 70){
                    para_with_break += "\n";
                    cur_len = 0;
                    ++num_lines;
                }
                para_with_break += para[k] + " ";
            }
            if(y_pos + 10 + 8 * num_lines >= 270){
                y_pos = 30;
                doc.addPage();
            }
            doc.text(20, y_pos, para_with_break);
            y_pos += 10 + 8 * num_lines;
        }
    }
}
function other_reqs(){
    var cur_div = whole.querySelector("#other_reqs");

    var rows = cur_div.querySelectorAll("*");
    for(i = 0; i < rows.length; ++i){
        if(rows[i].tagName === "H1"){
            doc.setFontSize(22);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 15;
        }
        else if(rows[i].tagName === "H3"){
            doc.setFontSize(15);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 10;
        }
        else if(rows[i].tagName === "P"){
            doc.setFontSize(12);
            var para = rows[i].textContent.split(" ");
            var para_with_break = "";
            var cur_len = 0;
            var num_lines = 0;
            for(k = 0; k < para.length; ++k){
                cur_len += para[k].length;
                if(cur_len >= 70){
                    para_with_break += "\n";
                    cur_len = 0;
                    ++num_lines;
                }
                para_with_break += para[k] + " ";
            }
            if(y_pos + 10 + 8 * num_lines >= 270){
                y_pos = 30;
                doc.addPage();
            }
            doc.text(20, y_pos, para_with_break);
            y_pos += 10 + 8 * num_lines;
        }
    }
}

function appendix_a(){
    var cur_div = whole.querySelector("#appendix");

    var rows = cur_div.querySelectorAll("*");
    for(i = 0; i < rows.length; ++i){
        if(rows[i].tagName === "H1"){
            doc.setFontSize(22);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 15;
        }
        else if(rows[i].tagName === "H3"){
            doc.setFontSize(15);
            doc.text(20, y_pos, rows[i].textContent);
            y_pos += 10;
        }
        else if(rows[i].tagName === "P"){
            doc.setFontSize(12);
            var para = rows[i].textContent.split(" ");
            var para_with_break = "";
            var cur_len = 0;
            var num_lines = 0;
            for(k = 0; k < para.length; ++k){
                cur_len += para[k].length;
                if(cur_len >= 70){
                    para_with_break += "\n";
                    cur_len = 0;
                    ++num_lines;
                }
                para_with_break += para[k] + " ";
            }
            if(y_pos + 10 + 8 * num_lines >= 270){
                y_pos = 30;
                doc.addPage();
            }
            doc.text(20, y_pos, para_with_break);
            y_pos += 10 + 8 * num_lines;
        }
    }
}

function generate(){
    frontPage();
    table_of_contents();
    introduction();
    overall_description();
    specific_requirements();
    non_functional_req();
    other_reqs();
    appendix_a();

    doc.save('SRS.pdf');
}





