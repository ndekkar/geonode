/**
 * @file Intake system parameter graph
 * configurations (Step 2 of create wizard)
 * @version 1.0
 */


// Program starts here. The document.onLoad executes the
// createEditor function with a given configuration.
// In the config file, the mxEditor.onInit method is
// overridden to invoke this global function as the
// last step in the editor constructor.
function onInit(editor) {
    // Enables rotation handle
    mxVertexHandler.prototype.rotationEnabled = true;

    // Enables guides
    mxGraphHandler.prototype.guidesEnabled = true;

    // Alt disables guides
    mxGuide.prototype.isEnabledForEvent = function(evt) {
        return !mxEvent.isAltDown(evt);
    };

    // Enables snapping waypoints to terminals
    mxEdgeHandler.prototype.snapToTerminals = true;

    // Defines an icon for creating new connections in the connection handler.
    // This will automatically disable the highlighting of the source vertex.
    mxConnectionHandler.prototype.connectImage = new mxImage('/static/mxgraph/images/connector.gif', 16, 16);

    // Enables connections in the graph and disables
    // reset of zoom and translate on root change
    // (ie. switch between XML and graphical mode).
    editor.graph.setConnectable(true);

    // Clones the source if new connection has no target
    editor.graph.connectionHandler.setCreateTarget(true);

    // Installs a popupmenu handler using local function (see below).
    editor.graph.popupMenuHandler.factoryMethod = function(menu, cell, evt){
        return createPopupMenu(editor.graph, menu, cell, evt);
    };

    // Updates the title if the root changes
    var title = document.getElementById('title');

    if (title != null) {
        var f = function(sender) {
            title.innerHTML = sender.getTitle();
        };

        editor.addListener(mxEvent.ROOT, f);
        f(editor);
    }

    // Changes the zoom on mouseWheel events
    /* mxEvent.addMouseWheelListener(function (evt, up) {
       if (!mxEvent.isConsumed(evt)) {
         if (up) {
           editor.execute('zoomIn');
         }
         else {
           editor.execute('zoomOut');
         }
 
         mxEvent.consume(evt);
       }
     });*/

    // Defines a new action to switch between
    // XML and graphical display
    var textNode = document.getElementById('xml');
    var graphNode = editor.graph.container;

    var sourceInput = document.getElementById('source');


    var getdata = document.getElementById('getdata');
    getdata.checked = false;

    var funct = function(editor) {
        if (getdata.checked) {
            //console.log(getdata.checked)
            graphNode.style.display = 'none';
            textNode.style.display = 'inline';

            var enc = new mxCodec();
            var node = enc.encode(editor.graph.getModel());

            textNode.value = mxUtils.getPrettyXml(node);
            textNode.originalValue = textNode.value;
            textNode.focus();
        } else {
            graphNode.style.display = '';

            if (textNode.value != textNode.originalValue) {
                var doc = mxUtils.parseXml(textNode.value);
                var dec = new mxCodec(doc);
                dec.decode(doc.documentElement, editor.graph.getModel());
            }

            textNode.originalValue = null;

            // Makes sure nothing is selected in IE
            if (mxClient.IS_IE) {
                mxUtils.clearSelection();
            }

            textNode.style.display = 'none';

            // Moves the focus back to the graph
            editor.graph.container.focus();
        }
    };

    /* var getd = function(editor){
         graphNode.style.display = 'none';
             textNode.style.display = 'inline';

             var enc = new mxCodec();
             var node = enc.encode(editor.graph.getModel());

             textNode.value = mxUtils.getPrettyXml(node);
             textNode.originalValue = textNode.value;
             textNode.focus();
     }*/

    editor.addAction('switchView', funct);

    // Defines a new action to switch between
    // XML and graphical display
    mxEvent.addListener(getdata, 'click', function() {
        editor.execute('switchView');
    });

    // Create select actions in page
    //var node = document.getElementById('mainActions');
    var buttons = ['group', 'ungroup', 'cut', 'copy', 'paste', 'delete', 'undo', 'redo', 'print', 'show'];

    // Only adds image and SVG export if backend is available
    // NOTE: The old image export in mxEditor is not used, the urlImage is used for the new export.
    if (editor.urlImage != null) {
        // Client-side code for image export
        var exportImage = function(editor) {
            var graph = editor.graph;
            var scale = graph.view.scale;
            var bounds = graph.getGraphBounds();

            // New image export
            var xmlDoc = mxUtils.createXmlDocument();
            var root = xmlDoc.createElement('output');
            xmlDoc.appendChild(root);

            // Renders graph. Offset will be multiplied with state's scale when painting state.
            var xmlCanvas = new mxXmlCanvas2D(root);
            xmlCanvas.translate(Math.floor(1 / scale - bounds.x), Math.floor(1 / scale - bounds.y));
            xmlCanvas.scale(scale);

            var imgExport = new mxImageExport();
            imgExport.drawState(graph.getView().getState(graph.model.root), xmlCanvas);

            // Puts request data together
            var w = Math.ceil(bounds.width * scale + 2);
            var h = Math.ceil(bounds.height * scale + 2);
            var xml = mxUtils.getXml(root);

            // Requests image if request is valid
            if (w > 0 && h > 0) {
                var name = 'export.png';
                var format = 'png';
                var bg = '&bg=#FFFFFF';

                new mxXmlRequest(editor.urlImage, 'filename=' + name + '&format=' + format +
                    bg + '&w=' + w + '&h=' + h + '&xml=' + encodeURIComponent(xml)).
                simulate(document, '_blank');
            }
        };

        editor.addAction('exportImage', exportImage);

        // Client-side code for SVG export
        var exportSvg = function(editor) {
            var graph = editor.graph;
            var scale = graph.view.scale;
            var bounds = graph.getGraphBounds();

            // Prepares SVG document that holds the output
            var svgDoc = mxUtils.createXmlDocument();
            var root = (svgDoc.createElementNS != null) ?
                svgDoc.createElementNS(mxConstants.NS_SVG, 'svg') : svgDoc.createElement('svg');

            if (root.style != null) {
                root.style.backgroundColor = '#FFFFFF';
            } else {
                root.setAttribute('style', 'background-color:#FFFFFF');
            }

            if (svgDoc.createElementNS == null) {
                root.setAttribute('xmlns', mxConstants.NS_SVG);
            }

            root.setAttribute('width', Math.ceil(bounds.width * scale + 2) + 'px');
            root.setAttribute('height', Math.ceil(bounds.height * scale + 2) + 'px');
            root.setAttribute('xmlns:xlink', mxConstants.NS_XLINK);
            root.setAttribute('version', '1.1');

            // Adds group for anti-aliasing via transform
            var group = (svgDoc.createElementNS != null) ?
                svgDoc.createElementNS(mxConstants.NS_SVG, 'g') : svgDoc.createElement('g');
            group.setAttribute('transform', 'translate(0.5,0.5)');
            root.appendChild(group);
            svgDoc.appendChild(root);

            // Renders graph. Offset will be multiplied with state's scale when painting state.
            var svgCanvas = new mxSvgCanvas2D(group);
            svgCanvas.translate(Math.floor(1 / scale - bounds.x), Math.floor(1 / scale - bounds.y));
            svgCanvas.scale(scale);

            var imgExport = new mxImageExport();
            imgExport.drawState(graph.getView().getState(graph.model.root), svgCanvas);

            var name = 'export.svg';
            var xml = encodeURIComponent(mxUtils.getXml(root));

            new mxXmlRequest(editor.urlEcho, 'filename=' + name + '&format=svg' + '&xml=' + xml).simulate(document, "_blank");
        };

        editor.addAction('exportSvg', exportSvg);

        buttons.push('exportImage');
        buttons.push('exportSvg');
    };

    for (var i = 0; i < buttons.length; i++) {
        var button = document.createElement('button');
        mxUtils.write(button, mxResources.get(buttons[i]));

        var factory = function(name) {
            return function() {
                editor.execute(name);
            };
        };

        mxEvent.addListener(button, 'click', factory(buttons[i]));
        //node.appendChild(button);
    }

    /* Create select actions in page
    var node = document.getElementById('selectActions');
    mxUtils.write(node, 'Select: ');
    mxUtils.linkAction(node, 'All', editor, 'selectAll');
    mxUtils.write(node, ', ');
    mxUtils.linkAction(node, 'None', editor, 'selectNone');
    mxUtils.write(node, ', ');
    mxUtils.linkAction(node, 'Vertices', editor, 'selectVertices');
    mxUtils.write(node, ', ');
    mxUtils.linkAction(node, 'Edges', editor, 'selectEdges');
    */
    // Create select actions in page
    /*var node = document.getElementById('zoomActions');
    mxUtils.write(node, 'Zoom: ');
    mxUtils.linkAction(node, 'In', editor, 'zoomIn');
    mxUtils.write(node, ', ');
    mxUtils.linkAction(node, 'Out', editor, 'zoomOut');
    mxUtils.write(node, ', ');
    mxUtils.linkAction(node, 'Actual', editor, 'actualSize');
    mxUtils.write(node, ', ');
    mxUtils.linkAction(node, 'Fit', editor, 'fit');*/


    //use jquery
    $(document).ready(function() {

        var graphData = [];
        var connetion = [];

        /**
         * Button to save 
         * data on graphData
         * xml on textxml
         */

        $('#inputMathAscii').keyup(function() {
            $('#RenderingMathAscii').text(`'math' ${$(this).val()} 'math'`);
            MathJax.typeset()
        });

        $('#ModalAddCostBtn').click(function() {

            $('#VarCostListGroup div').remove();
            for (const index of graphData) {
                tmp = JSON.parse(index.varcost);
                $('#VarCostListGroup').append(`
                <div class="panel panel-info">
                    <div class="panel-heading">
                        <h4 class="panel-title">
                            <a data-toggle="collapse" data-parent="#VarCostListGroup" href="#VarCostListGroup_${index.id}">${index.id} - ${ index.name }</a>
                        </h4>
                    </div>
                    <div id="VarCostListGroup_${index.id}" class="panel-collapse collapse">
                        <div class="panel-body">
                        <a href="#" class="list-group-item list-group-item-action">${tmp[0]}</a>
                        <a href="#" class="list-group-item list-group-item-action">${tmp[1]}</a>
                        <a href="#" class="list-group-item list-group-item-action">${tmp[2]}</a>
                        <a href="#" class="list-group-item list-group-item-action">${tmp[3]}</a>
                        <a href="#" class="list-group-item list-group-item-action">${tmp[4]}</a>
                        <a href="#" class="list-group-item list-group-item-action">${tmp[5]}</a>
                        <a href="#" class="list-group-item list-group-item-action">${tmp[6]}</a>
                        <a href="#" class="list-group-item list-group-item-action">${tmp[7]}</a>
                        <a href="#" class="list-group-item list-group-item-action">${tmp[8]}</a>
                        <a href="#" class="list-group-item list-group-item-action">${tmp[9]}</a>
                        </div>
                    </div>
                </div>
                `);
            }
            /*
            for (let index = 0; index < graphData.length; index++) {
                tmp = JSON.parse(graphData[index].varcost)
                $('#VarCostListGroup').html(`
                <div class="list-group">
                    <a href="#" class="list-group-item list-group-item-action active">
                        ${ graphData[index].name }
                    </a>
                    <a href="#" class="list-group-item list-group-item-action">${tmp[0]}</a>
                    <a href="#" class="list-group-item list-group-item-action">${tmp[1]}</a>
                    <a href="#" class="list-group-item list-group-item-action">${tmp[2]}</a>
                    <a href="#" class="list-group-item list-group-item-action">${tmp[3]}</a>
                    <a href="#" class="list-group-item list-group-item-action">${tmp[4]}</a>
                    <a href="#" class="list-group-item list-group-item-action">${tmp[5]}</a>
                    <a href="#" class="list-group-item list-group-item-action">${tmp[6]}</a>
                    <a href="#" class="list-group-item list-group-item-action">${tmp[7]}</a>
                    <a href="#" class="list-group-item list-group-item-action">${tmp[8]}</a>
                    <a href="#" class="list-group-item list-group-item-action">${tmp[9]}</a>
                </div>
                `)
            }*/

        });


        $('#saveGraph').click(function() {
            var enc = new mxCodec();
            var node = enc.encode(editor.graph.getModel());
            graphData = [];
            connetion = [];
            node.querySelectorAll('Symbol').forEach(function(node) {
                graphData.push({
                    'id': node.id,
                    "name": node.getAttribute('name'),
                    'external': node.getAttribute('externalData'),
                    'resultdb': node.getAttribute('resultdb'),
                    'quantity': node.getAttribute('quantity'),
                    'varcost': node.getAttribute('varcost'),
                })
            });

            node.querySelectorAll('mxCell').forEach(function(node) {
                if (node.id != "") {
                    connetion.push({
                        'id': node.id,
                        'source': node.getAttribute('source'),
                        'target': node.getAttribute('target'),
                    })
                }

            });



            console.log(graphData);
            //console.log(textxml);
            //console.log(connetion);
        });


        //load data when add an object in a diagram
        editor.graph.addListener(mxEvent.ADD_CELLS, function(sender, evt) {

            var selectedCell = evt.getProperty("cells");
            var idvar = selectedCell[0].id;
            if (selectedCell != undefined) {
                var varcost = [];
                varcost.push(
                    `Q_${idvar}`,
                    `CSed_${idvar}`,
                    `CN_${idvar}`,
                    `CP_${idvar}`,
                    `WSed_${idvar}`,
                    `WN_${idvar}`,
                    `WP_${idvar}`,
                    `WSed_ret_${idvar}`,
                    `WN_ret_${idvar}`,
                    `WP_ret_${idvar}`
                );
                selectedCell[0].setAttribute('varcost', JSON.stringify(varcost));

                $.ajax({
                    url: `/intake/loadProcess/${selectedCell[0].dbreference}`,
                    success: function(result) {
                        selectedCell[0].setAttribute("resultdb", result);
                    }
                });
            }

            if (selectedCell[0].dbreference == 'EXTERNALINPUT') {
                //Si se añade un elemento externo
            }

        });

        /**  
         * Global variables for save data 
         * @param {Array} resultdb   all data from DB
         * @param {Object} selectedCell  cell selected from Diagram 
         */

        var resultdb = [];
        var selectedCell;
        var notConnectedCells = [];
        var parentCellId = "2";

        //Load data from figure to html
        editor.graph.addListener(mxEvent.CLICK, function(sender, evt) {
            selectedCell = evt.getProperty("cell");
            if (selectedCell != undefined) {
                resultdb = JSON.parse(selectedCell.getAttribute('resultdb'));
                $('#titleDiagram').text(resultdb[0].fields.categorys);
                // Add Value to Panel Information Right on HTML
                $('#sedimentosDiagram').val(resultdb[0].fields.predefined_sediment_perc);
                $('#nitrogenoDiagram').val(resultdb[0].fields.predefined_nitrogen_perc);
                $('#fosforoDiagram').val(resultdb[0].fields.predefined_phosphorus_perc);
                // Add Validator 
                $('#sedimentosDiagram').attr('min', resultdb[0].fields.minimal_sediment_perc);
                $('#sedimentosDiagram').attr('max', resultdb[0].fields.maximal_sediment_perc);
                $('#nitrogenoDiagram').attr('min', resultdb[0].fields.minimal_nitrogen_perc);
                $('#nitrogenoDiagram').attr('max', resultdb[0].fields.maximal_nitrogen_perc);
                $('#fosforoDiagram').attr('min', resultdb[0].fields.minimal_phosphorus_perc);
                $('#fosforoDiagram').attr('max', resultdb[0].fields.maximal_phosphorus_perc);
            }
        });

        //Add value entered in sediments in the field resultdb
        $('#sedimentosDiagram').keyup(function() {
            resultdb[0].fields.predefined_sediment_perc = $('#sedimentosDiagram').val();
            selectedCell.setAttribute('resultdb', JSON.stringify(resultdb));
        });

        //Add value entered in nitrogen in the field resultdb
        $('#nitrogenoDiagram').keyup(function() {
            resultdb[0].fields.predefined_nitrogen_perc = $('#nitrogenoDiagram').val();
            selectedCell.setAttribute('resultdb', JSON.stringify(resultdb));
        });

        //Add value entered in phosphorus in the field resultdb
        $('#fosforoDiagram').keyup(function() {
            resultdb[0].fields.predefined_phosphorus_perc = $('#fosforoDiagram').val();
            selectedCell.setAttribute('resultdb', JSON.stringify(resultdb));
        });

        function Validate(mxCell) {
            let isConnected = true;
            // check each cell that each edge connected to
            for (let i = 0; i < mxCell.getEdgeCount(); i++) {
                let edge = mxCell.getEdgeAt(i);

                if (edge.target === null) continue; // no target
                if (mxCell.getId() === edge.target.getId()) continue; // target is mxCell itself

                isConnected = edge.source !== null && edge.target !== null;
                if (isConnected) {
                    // remove source cell if found and so on
                    let sourceIndex = notConnectedCells.findIndex(c => c.id === edge.source.getId());
                    if (sourceIndex !== -1) notConnectedCells.splice(sourceIndex, 1);

                    let targetIndex = notConnectedCells.findIndex(c => c.id === edge.target.getId());
                    if (targetIndex !== -1) notConnectedCells.splice(targetIndex, 1);

                    let edgeIndex = notConnectedCells.findIndex(c => c.id === edge.getId());
                    if (edgeIndex !== -1) notConnectedCells.splice(edgeIndex, 1);

                    // check next cell and its edges
                    Validate(edge.target);
                }
            }
        }

        function ResetColor(state) {
            state.shape.node.classList.remove("not_connected");
            if (state.text)
                state.text.node.classList.remove("not_connected");
        }

        function SetNotConnectedColor(state) {
            for (let i = 0; i < notConnectedCells.length; i++) {
                let mxCell = notConnectedCells[i];
                let state = graphView.getState(mxCell);
                state.shape.node.classList.add("not_connected");
                if (state.text)
                    state.text.node.classList.add("not_connected");
            }
        }

        document.querySelector("#validate_btn").addEventListener("click", function() {

            let cells = editor.graph.getModel().cells;
            graphView = editor.graph.getView();
            notConnectedCells.length = 0;
            console.log(cells)
            console.log(graphView)

            // create an array of cells and reset the color
            for (let key in cells) {
                if (!cells.hasOwnProperty(key)) continue;

                let mxCell = cells[key];
                if (!mxCell.isVertex() && !mxCell.isEdge()) continue;
                notConnectedCells.push(mxCell);
                let state = graphView.getState(mxCell);

                console.log(state)
                ResetColor(state);
            }

            // starts with the parent cell
            let parentCell = notConnectedCells.find(c => c.id === parentCellId);
            Validate(parentCell);

            SetNotConnectedColor();
        })

    });

}