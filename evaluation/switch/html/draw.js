

// Builds the HTML Table out of myList.
function buildHtmlTable(selector) {

    $.getJSON("http://www.princeton.edu/~hyojoonk/switch/out.json", function(data) { 
    
        // this will show the info it in firebug console 
//        console.log(data); 

        var columns = addAllColumnHeaders(data, selector);
//        console.log(columns); 
    
        for (var i = 0 ; i < data.length ; i++) {
            var row$ = $('<tr/>');

            $.each(columns, function(index, value) {
                var cellValue = data[i][value]

                if (cellValue == null) { cellValue = ""; }
                else if (cellValue == "O") { row$.css('background-color','#33CC33'); }
                else if (cellValue == "X") { row$.css('background-color','#FF3333'); }

                row$.append($('<td/>').html(cellValue));
            });
            $("#excelDataTable").append(row$);

            // At the end, check next. If match, make a line.
            if (i < data.length-1) {
                cat_now = data[i]['Category']
                cat_nxt = data[i+1]['Category']

                if (cat_now != cat_nxt) {
                    var rowextra$ = $('<tr/>');
                    $.each(columns, function(index, value) {
                        var cellValueextra = "--"
                        rowextra$.css('background-color','#000000');
                        rowextra$.append($('<td/>').html(cellValueextra));
                    });
                    $("#excelDataTable").append(rowextra$);
                }
            }
        }
    }); 
}

// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records
function addAllColumnHeaders(myList)
{
    var columnSet = [];
    var headerTr$ = $('<tr/>');

    for (var i = 0 ; i < myList.length ; i++) {
        var rowHash = myList[i];
        for (var key in rowHash) {
            if ($.inArray(key, columnSet) == -1){
                columnSet.push(key);
            }
        }
    }
    
    columnSet.sort();
    $.each(columnSet, function(index, value) {
        headerTr$.append($('<th/>').html(value));
    });

    $("#excelDataTable").append(headerTr$);

    return columnSet;
}
