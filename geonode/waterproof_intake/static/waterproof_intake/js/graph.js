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
            console.log(getdata.checked)
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


        $('#saveGraph').click(function() {
            var enc = new mxCodec();
            var node = enc.encode(editor.graph.getModel());
            var graphData = [];

            node.querySelectorAll('Symbol').forEach(function(node) {
                graphData.push({
                    'id': node.id,
                    "name": node.getAttribute('name'),
                    'external': node.getAttribute('externalData'),
                })

            });

            console.log(graphData);
        });

        function loadData(data) {

            $('#titleDiagram').text(data[0].fields.categorys);
            $('#sedimentosDiagram').val(data[0].fields.predefined_sediment_perc);
            $('#nitrogenoDiagram').val(data[0].fields.predefined_nitrogen_perc);
            $('#fosforoDiagram').val(data[0].fields.predefined_phosphorus_perc);
            console.log(data);

        }


        var nombrep = $("#title");

        editor.graph.addListener(mxEvent.CLICK, function(sender, evt) {

            //get the xml save in (node)
            var enc = new mxCodec();

            var selectedCell = evt.getProperty("cell");

            if (selectedCell != undefined) {
                $.ajax({
                    url: `/intake/loadProcess/${selectedCell.getAttribute('dbreference')}`,
                    success: function(result) {
                        var info = JSON.parse(result);
                        loadData(info);
                    }
                });
            }



            //
            //console.log(node);
            /*
                        //get xml like text
                        textNode.value = mxUtils.getPrettyXml(node);
                        //console.log(textNode.value)

                        //get cell
                        var selectedCell = evt.getProperty("cell");
                        //console.log(selectedCell);

                        //set attributes
                        selectedCell.setAttribute("parametrop", "45");

                        

                        //object to save the attribute
                        var graphData = [];
                        //get element ('symbol') from xml (node)
                        //console.log(node.querySelectorAll('Symbol'))
                        node.querySelectorAll('Symbol').forEach(function(node) {
                            console.log(node)
                            graphData.push({
                                'id': node.id,
                                "name": node.getAttribute('name'),
                                'external': node.getAttribute('externalData'),
                            })

                        });
                        console.log(graphData)
                        */

            /** 
             * Get filtered activities by transition id 
             * @param {String} url   activities URL 
             * @param {Object} data  transition id  
             *
             * @return {String} activities in HTML option format
             */
            /*
            
            */

            //put title on right view
            /*if (selectedCell.style != undefined) {
                console.log(selectedCell.name);
                nombrep.empty();
                nombrep.append(selectedCell.name);
            }*/

        });
    });



}