$(document).ready(function() {
    var isDrawing = false;
    var cueBallCenter = { x: 0, y: 0 };
    var currentSVGIndex = 0;
    var totalSVGs = $('#svgContainer svg').length;

    $('#svgContainer svg').hide().first().show();
    var animationTimer = setInterval(animateSVGs, 100);

    $(document).mousedown(startDrawing);
    $(document).mouseup(endDrawing);
    $(document).mousemove(updateDrawing);

    function startDrawing(event) {
        isDrawing = true;
        var cueBall = $('circle[fill="WHITE"]');
        cueBallCenter = {
            x: parseFloat(cueBall.attr('cx')),
            y: parseFloat(cueBall.attr('cy'))
        };
        $('#line').show();
        updateLine(event.pageX, event.pageY);
    }

    function endDrawing(event) {
        if (!isDrawing) return;
        
        isDrawing = false;
        $('#line').hide();

        var velocity = calculateVelocity(event.pageX, event.pageY);
        console.log("Velocity x:", velocity.x, "Velocity y:", velocity.y);

        sendShotData(velocity);
        fetchAnimation();
    }

    function updateDrawing(event) {
        if (!isDrawing) return;
        updateLine(event.pageX, event.pageY);
    }

    function calculateVelocity(mouseX, mouseY) {
        var scale_factor = 10;
        return {
            x: (mouseX * 2 - 25 - cueBallCenter.x) * scale_factor,
            y: (mouseY * 2 - 25 - cueBallCenter.y) * scale_factor
        };
    }

    function sendShotData(velocity) {
        $.ajax({
            type: "POST",
            url: '/shot',
            contentType: "application/json",
            data: JSON.stringify(velocity),
            success: function() { console.log("Shot data sent successfully."); },
            error: function(xhr, status, error) { console.error("Error sending shot data:", error); }
        });
    }

    function fetchAnimation() {
        $.ajax({
            type: "GET",
            url: 'animate.html',
            success: function(data) {
                if (data.trim()) {
                    window.location.href = 'animate.html';
                } else {
                    console.log("animate.html is empty");
                }
            },
            error: function(xhr, status, error) {
                console.error("Error fetching animate.html:", error);
            }
        });
    }

    function updateLine(mouseX, mouseY) {
        $('#line').attr({
            'x1': cueBallCenter.x,
            'y1': cueBallCenter.y,
            'x2': mouseX * 2 - 25,
            'y2': mouseY * 2 - 25
        });
    }

    function animateSVGs() {
        if (currentSVGIndex >= totalSVGs) {
            clearInterval(animationTimer);
            return;
        }
        $('#svgContainer svg').hide().eq(currentSVGIndex++).show();
    }
});
