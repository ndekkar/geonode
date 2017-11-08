mapModule
    .factory('BoxDrawTool', BoxDrawTool);

BoxDrawTool.$inject = ['mapService'];

function BoxDrawTool(mapService) {
    var isBoxDrawn = false;
    var topRightFeature = null;
    var bottomRightFeature = null;
    var topLeftFeature = null;
    var bottomLeftFeature = null;
    var boxTopLeft, boxTopRight, boxBottomRight, boxBottomLeft;
    return function(map) {
        var map = map || mapService.getMap();
        var dragFeature = null;
        var resizeFeature = null;
        var dragCoordinate = null;
        var dragCursor = 'pointer';
        var dragPrevCursor = null;


        var STROKE_WIDTH = 3,
            CIRCLE_RADIUS = 5;

        var FILL_COLOR = 'rgba(255, 255, 255, 0.5)',
            STROKE_COLOR = 'rgba(0, 60, 136, 0.8)';
        var TRANSPARENT_COLOR = 'rgba(0, 0, 0, 0.1)';

        var lineStyle = new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: STROKE_COLOR,
                width: STROKE_WIDTH
            }),
            fill: new ol.style.Fill({
                color: FILL_COLOR
            })
        });

        var verticeStyle = new ol.style.Style({
            image: new ol.style.Circle({
                radius: CIRCLE_RADIUS,
                stroke: new ol.style.Stroke({
                    color: STROKE_COLOR,
                    width: STROKE_WIDTH
                }),
                fill: new ol.style.Fill({
                    color: FILL_COLOR
                })
            }),
            geometry: function(feature) {
                var coordinates = feature.getGeometry().getCoordinates();
                return new ol.geom.MultiPoint(coordinates[0]);
            }
        });

        var transparentCircleStyle = new ol.style.Style({
            image: new ol.style.Circle({
                radius: CIRCLE_RADIUS,
                stroke: new ol.style.Stroke({
                    color: TRANSPARENT_COLOR,
                    width: STROKE_WIDTH
                }),
                fill: new ol.style.Fill({
                    color: TRANSPARENT_COLOR
                })
            })
        });

        var features = new ol.Collection();
        features.on('add', function(event) {
            var feature = event.element;
            feature.set('id', 'bounding-box');
        });

        var vectorSource = new ol.source.Vector({
            features: features,
        });
        var featureOverlay = new ol.layer.Vector({
            source: vectorSource,
            style: [verticeStyle, lineStyle]
        });

        mapService.addVectorLayer(featureOverlay);

        function updateGeometry(feature) {
            var geometry = feature.getGeometry();
            geometry.setCoordinates([
                [boxTopLeft, boxBottomLeft, boxBottomRight, boxTopRight, boxTopLeft]
            ]);
        }

        function updateTopRight(feature, coordinate) {
            boxTopLeft = [boxTopLeft[0], coordinate[1]];
            boxTopRight = coordinate;
            boxBottomRight = [coordinate[0], boxBottomRight[1]];
            // boxBottomLeft =  [end[0], start[1]];
            topLeftFeature.getGeometry().setCoordinates(boxTopLeft);
            bottomRightFeature.getGeometry().setCoordinates(boxBottomRight);
            updateGeometry(feature);
        }

        function updateBottomLeft(feature, coordinate) {
            boxTopLeft = [coordinate[0], boxTopLeft[1]];
            // boxTopRight = coordinate;
            boxBottomRight = [boxBottomRight[0], coordinate[1]];
            boxBottomLeft = coordinate;
            topLeftFeature.getGeometry().setCoordinates(boxTopLeft);
            bottomRightFeature.getGeometry().setCoordinates(boxBottomRight);
            updateGeometry(feature);
        }

        function updateBottomRight(feature, coordinate) {
            // boxTopLeft = [coordinate[0], boxTopLeft[1]];
            boxTopRight = [coordinate[0], boxTopRight[1]];
            boxBottomRight = coordinate;
            boxBottomLeft = [boxBottomLeft[0], coordinate[1]];
            bottomLeftFeature.getGeometry().setCoordinates(boxBottomLeft);
            topRightFeature.getGeometry().setCoordinates(boxTopRight);
            updateGeometry(feature);
        }

        function updateTopLeft(feature, coordinate) {
            boxTopLeft = coordinate;
            boxTopRight = [boxTopRight[0], coordinate[1]];
            // boxBottomRight = coordinate;
            boxBottomLeft = [coordinate[0], boxBottomLeft[1]];
            bottomLeftFeature.getGeometry().setCoordinates(boxBottomLeft);
            topRightFeature.getGeometry().setCoordinates(boxTopRight);
            updateGeometry(feature);
        }

        var dragInteraction = new ol.interaction.Pointer({
            handleDownEvent: function(event) {
                var feature = map.forEachFeatureAtPixel(event.pixel,
                    function(feature, layer) {
                        return feature;
                    }
                );

                if (feature && feature.get('id') === 'bounding-box') {
                    dragCoordinate = event.coordinate;
                    parentFeature = feature.get('parentFeature');
                    if (parentFeature) {
                        resizeFeature = feature;
                    } else {
                        dragFeature = feature;
                    }
                    return true;
                }
                return false;
            },
            handleDragEvent: function(event) {
                var geometry, parentFeature, updateFn;
                var deltaX = event.coordinate[0] - dragCoordinate[0];
                var deltaY = event.coordinate[1] - dragCoordinate[1];
                if (resizeFeature) {
                    geometry = resizeFeature.getGeometry();
                    parentFeature = resizeFeature.get('parentFeature');
                    updateFn = resizeFeature.get('updateFn');
                } else {
                    geometry = dragFeature.getGeometry();
                }
                geometry.translate(deltaX, deltaY);

                if (updateFn) {
                    updateFn(parentFeature, event.coordinate);
                } else {
                    topLeftFeature.getGeometry().translate(deltaX, deltaY);
                    topRightFeature.getGeometry().translate(deltaX, deltaY);
                    bottomLeftFeature.getGeometry().translate(deltaX, deltaY);
                    bottomRightFeature.getGeometry().translate(deltaX, deltaY);

                    coordinates = geometry.getCoordinates()[0];
                    boxTopLeft = coordinates[0];
                    boxBottomLeft = coordinates[1];
                    boxBottomRight = coordinates[2];
                    boxTopRight = coordinates[3];
                }
                dragCoordinate[0] = event.coordinate[0];
                dragCoordinate[1] = event.coordinate[1];
            },
            handleMoveEvent: function(event) {
                if (dragCursor) {
                    var map = event.map;

                    var feature = map.forEachFeatureAtPixel(event.pixel,
                        function(feature, layer) {
                            return feature;
                        });

                    var element = event.map.getTargetElement();

                    if (feature) {
                        if (element.style.cursor != dragCursor) {
                            dragPrevCursor = element.style.cursor;
                            element.style.cursor = dragCursor;
                        }
                    } else if (dragPrevCursor !== undefined) {
                        element.style.cursor = dragPrevCursor;
                        dragPrevCursor = undefined;
                    }
                }
            },
            handleUpEvent: function(event) {
                dragCoordinate = null;
                dragFeature = null;
                resizeFeature = null;
                boundingBox = [boxTopLeft, boxBottomLeft, boxBottomRight, boxTopRight, boxTopLeft];
                // $scope.executeQuery($scope.queryStr);
                return false;
            }
        });

        // mapService.addInteraction(dragInteraction);

        var drawInteraction = new ol.interaction.Draw({
            features: features,
            type: 'LineString',
            geometryFunction: geometryFunction,
            maxPoints: 2
        });


        function geometryFunction(coordinates, geometry) {

            var start = coordinates[0];
            var end = coordinates[1];

            if (!geometry) {
                geometry = new ol.geom.Polygon(null);
            }
            boxTopLeft = start;
            boxBottomLeft = [start[0], end[1]];
            boxBottomRight = end;
            boxTopRight = [end[0], start[1]];
            // geometry.setCoordinates([
            //     [start, [start[0], end[1]], end, [end[0], start[1]], start]
            // ]);

            geometry.setCoordinates([
                [boxTopLeft, boxBottomLeft, boxBottomRight, boxTopRight, boxTopLeft]
            ]);

            return geometry;
        }


        drawInteraction.on('drawend', function(event) {
            boundingBox = event.feature.getGeometry().getCoordinates()[0];
            mapService.removeInteraction(drawInteraction);
            // $scope.executeQuery($scope.queryStr);

            topRightFeature = new ol.Feature({
                geometry: new ol.geom.Point(boxTopRight),
                coordinate: event.coordinate,
                name: 'topRightFeature',
                parentFeature: event.feature,
                updateFn: updateTopRight
            });
            topLeftFeature = new ol.Feature({
                geometry: new ol.geom.Point(boxTopLeft),
                coordinate: event.coordinate,
                name: 'topLeftFeature',
                parentFeature: event.feature,
                updateFn: updateTopLeft
            });
            bottomLeftFeature = new ol.Feature({
                geometry: new ol.geom.Point(boxBottomLeft),
                coordinate: event.coordinate,
                name: 'bottomLeftFeature',
                parentFeature: event.feature,
                updateFn: updateBottomLeft
            });
            bottomRightFeature = new ol.Feature({
                geometry: new ol.geom.Point(boxBottomRight),
                coordinate: event.coordinate,
                name: 'bottomRightFeature',
                parentFeature: event.feature,
                updateFn: updateBottomRight
            });

            topLeftFeature.setStyle(transparentCircleStyle);
            topRightFeature.setStyle(transparentCircleStyle);
            bottomLeftFeature.setStyle(transparentCircleStyle);
            bottomRightFeature.setStyle(transparentCircleStyle);

            vectorSource.addFeature(topLeftFeature);
            vectorSource.addFeature(topRightFeature);
            vectorSource.addFeature(bottomLeftFeature);
            vectorSource.addFeature(bottomRightFeature);
        });
        this.Draw = function() {
            mapService.addInteraction(dragInteraction);
            if (!isBoxDrawn) {
                mapService.addInteraction(drawInteraction);
                isBoxDrawn = true;
            }
        };

        this.Stop = function() {
            mapService.removeInteraction(dragInteraction);
        };
    };
}