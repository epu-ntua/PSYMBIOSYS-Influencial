/**
 * Created by user on 1/7/2016.
 */

/**
 * Created by Aggelos on 12/28/2015.
 */

/****************** For index *******************************/

// Global vars

var $prevInfluencerClicked = null,
    prevPageFetched = 1;


function activateBackdropHover() {

    $('.portfolio-item > .item-image').each(function () {
        $(this).hoverdir({
            hoverDelay: 75
        });
    });
}

activateBackdropHover();

$(document).ready(function() {

    $('#influencer-list').mixItUp();

    $("#twit").owlCarousel({

        navigation : true, // Show next and prev buttons
        slideSpeed : 100,
        paginationSpeed : 400,
        navigationText : false,
        singleItem: true,
        autoPlay: true,
        pagination: false
    });

    $("#client-speech").owlCarousel({

        autoPlay: 5000, //Set AutoPlay to 3 seconds
        stopOnHover: true,
        singleItem:true
    });

    $("#get-started").on('click', function(evt) {

        evt.preventDefault();
        $('html,body').animate({
          scrollTop: $("#main-content").offset().top
        }, 1500);
    });

    $("#learn-more").on('click', function(evt) {

        evt.preventDefault();
        $('html,body').animate({
          scrollTop: $("#testimonials").offset().top
        }, 1500);
    });

    $('.checkbox-tweetfluence.check-all-container').on('click', function(e) {

        e.preventDefault();

        var $this = $(this),
            check = $this.data('check'),
            $loadMore = $('#load-more'),
            $checkboxes = $('.checkbox-tweetfluence.checkbox-' + check)
                            .find('input'),
            prevVal = $this
                        .find('input')
                        .prop('checked');

        if (prevVal)
            $loadMore.hide();
        else
            $loadMore.show();
        $.each($checkboxes, function(i, checkbox) {
            $($checkboxes).prop('checked', !prevVal)
        });

        handleTopicFiltering(check)
    })

});

// Toggle the analytics section for an influencer

$('.toggle-analytics').on('click', function(evt) {
    handleAnalytics(evt, $(this));

});

// Change between Charts

$( ".btn-chart-select" ).on('click', function() {

    var $this = $(this);
    var $analyticsContainer = $this
        .parents('.influencer-analytics');

    var $averagesChart = $analyticsContainer
        .find('.averages-chart');

    var $timelineChart = $analyticsContainer
        .find('.timeline-chart');

    var $chartToShow = ($this.text() == 'Averages') ? $averagesChart : $timelineChart;
    var $chartToHide = ($this.text() == 'Averages') ? $timelineChart : $averagesChart;

    $analyticsContainer
        .find('.btn-chart-select')
        .removeClass('active');

    $this.addClass('active');

    $chartToHide.fadeOut( "slow", function() {

        $chartToHide.css('display', 'none');
        $chartToShow.css('display', 'block');
        $chartToShow.fadeIn( "slow", function() {});

    });
});


// Topic Filtering
$('.topic-filter').on('click', function() {
    handleTopicFiltering('topic')
});
$('.network-filter').on('click', function() {
    handleTopicFiltering('network')
});


// Snippet to load more influencers when the button is clicked
$('#load-more').on('click', function(e) {

    e.preventDefault();
    prevPageFetched ++;
    var $this = $(this);

    $.ajax({
        type: "get",
        data: {page: prevPageFetched},
        cache: false,
        url: 'influencers',
        error: function (xhr, status, error) {
            console.log('An error has occured. ' + status);
        },
        success: function (response) {
            if (response) {

                $('#influencer-list').append(response);

                $('.toggle-analytics').off().on('click', function(evt) {
                    handleAnalytics(evt, $(this));
                    activateBackdropHover();
                })
            }
        }
    })

});

function handleTopicFiltering(filter_type) {

    // Fetch all clicked Topics and insert them in a list
    var filter;
    var filters = [];
    var $checked = $('.' + filter_type + '-filter:checked');

    $.each($checked, function (i, checkbox) {
        filter = $(checkbox)
            .parents('.checkbox-tweetfluence')
            .find('.checkbox-text')
            .text();

        filters.push(filter)
    });

    // Fetch all Influencers Container that match at least one of the topics checked

    var displayed = $('.influencer-container')
        .filter(function () {
            return checkFilterExistance(this, filters, filter_type)
        });
    console.log(displayed)
    $('#influencer-list').mixItUp('filter', displayed);

    $('.influencer-analytics').slideUp('slow')
}


function checkFilterExistance(selector, topics, filter_type) {

    var topicFound = false;
    var topic;

    if (filter_type == 'topic') {
        var $topicSpans = $(selector).find('.influence-topic span');

        $.each($topicSpans, function (i, topicSpan) {
            topic = $(topicSpan).text();

            if (inList(topic, topics)) {
                topicFound = true;
                return false
            }
        })
    }
    else {
        var $socialNetwork = $(selector).find('.social-network');

        $.each(topics, function (i, topic) {
            if($socialNetwork.hasClass('fa-' + topic)) {
                topicFound = true;
                return false
            }
        })
    }


    return topicFound
}

// Checks whether String exists inside the List
function inList(psString, psList)
{
    var laList = psList;

    var i = laList.length;
    while (i--) {
        if (laList[i] === psString) return true;
    }
    return false;
}

// Chart Draw
function drawAveragesChart(data, container) {

    var $prevSvg = $('.averages-chart').find('svg');
    if ($prevSvg.length)
        $prevSvg.remove();

    var newData = data['topics_averages'];
    var topics = $(container).find('.influence-topic span');

    for (var i=0;i<data['topics_averages'].length;i++)
        newData[i]['name'] = topics.eq(i).text();

    var svg = dimple.newSvg('.averages-chart', "100%", "243px");
    var chart = new dimple.chart(svg, newData);

    chart.setBounds('85px', '30px', '80%', '65%');
    var x = chart.addCategoryAxis("x", "name");
    var y = chart.addMeasureAxis("y", "average_score");
    var series = chart.addSeries("name", dimple.plot.bar);
    x.title = '';
    y.title = 'Intensity';
    y.ticks = 6;
    x.fontSize = '6px';

    series.barGap = 0.6;
    chart.draw();

    // Due to the fact that this chart is originally hidden. Its title is shifted right so we correct it here
    $('.averages-chart text.dimple-custom-axis-titledimple-axis-y').attr('y', '70px');


    $(window).on('resize', function () {
        chart.draw(0, false);
        $('.averages-chart text.dimple-custom-axis-titledimple-axis-y').attr('y', '90px');
    });
}

function drawTimelineChart(data, container) {

    var $prevSvg = $('.timeline-chart').find('svg');
    if ($prevSvg.length)
        $prevSvg.remove();

    var newData = data['topics_values'];
    var topics = $(container).find('.influence-topic span');
    var prevTopic = '';
    var counter = -1;

    for (var i=0;i<data['topics_values'].length;i++) {

        if ((prevTopic == '') || (prevTopic != data['topics_values'][i]['name'])) {
            counter += 1;
            prevTopic = data['topics_values'][i]['name'];
        }
        newData[i]['name'] = topics.eq(counter).text();
    }

    var svg = dimple.newSvg('.timeline-chart', "95%", "243px");
    var chart = new dimple.chart(svg, newData);

    chart.setBounds('8%', '60px', '85%', '60%');
    var x =chart.addTimeAxis("x", "start", '%Y-%m-%d', '%b %e');
    var y = chart.addMeasureAxis("y", "score");
    var series = chart.addSeries("name", dimple.plot.line);

    x.title = '';
    x.timePeriod = d3.time.weeks;
    y.title = 'Intensity';
    y.ticks = 6;

    chart.addLegend('8%', '20px', '85%', '50px', 'left');
    chart.draw();

    $(window).on('resize', function () {
        chart.draw(0, true);
    });
}


function updateTopTopics(container) {

    var $topTopics = $('.portfolio-item-list')
        .find('.influencer-analytics')
        .find('.top-topics')
        .children('p'),
        $topicsToShow = $(container).
            find('.influence-topic span');

    $.each($topTopics, function(i, topTopic) {
        $(topTopic).text($topicsToShow.eq(i).text());
    })
}


function drawAnalytics($container) {

    var influencerId = $container
        .find('.influencer')
        .data('influencer-id');

    $.ajax({
        type: "get",
        data: {},
        cache: false,
        url: 'spark/influencers/' + influencerId ,
        dataType: "json",
        error: function (xhr, status, error) {
            console.log('An error has occured. ' + status);
        },
        success: function (response) {
            drawAveragesChart(response, $container);
            drawTimelineChart(response, $container);
            updateTopTopics($container)
        }
    })
}


// Returns md, sm or xs depending on window size
function evaluateCol(window) {

    var $window = $(window);
    var currentWidth = $window.width();

    if (currentWidth <= 767)
        return 'xs';
    else if (currentWidth <= 991)
        return 'sm';
    else
        return 'md'


}

// Finds out where to append the analytic box so its right under the influencer clicked. This changes based on window
// size, since the number of influencers in a given row changes

function selectorToAppendAnalytics($container) {

    var colWidth = evaluateCol(window);
    var influencerPositionInRow = $container.index('.influencer-container:visible');

    switch (colWidth) {
        case 'xs':
            return lastInfluencerInRow(influencerPositionInRow, 1);

        case 'sm':
            return lastInfluencerInRow(influencerPositionInRow, 3);

        case 'md':
            return lastInfluencerInRow(influencerPositionInRow, 4);
    }
}

// Find the last of each row. The row isn't a bootstrap row but a visual row of elements
function lastInfluencerInRow( influencerIndex, influencersInRow) {

    var totalInfluencers = $('.influencer:visible').length;
    var indexToReturn = influencersInRow * (Math.floor(influencerIndex / influencersInRow) + 1);

    if (indexToReturn > totalInfluencers)
        indexToReturn = totalInfluencers;

    indexToReturn-- ;

    return $('.influencer-container:visible:eq(' + indexToReturn + ')')
}

function toggleSearchFaIcon($influencer) {

    if ($influencer == null) return;

    var $faIcon = $influencer.find('.item-image i');

    ($faIcon.hasClass('fa-search-plus'))
        ? $faIcon.removeClass('fa-search-plus').addClass('fa-search-minus')
        : $faIcon.removeClass('fa-search-minus').addClass('fa-search-plus');
}

function toggleActiveInfluencer($influencer) {

    ($influencer.hasClass('influencer-active'))
        ? $influencer.removeClass('influencer-active')
        : $influencer.addClass('influencer-active');

    $('.influencer')
        .not($influencer)
        .removeClass('influencer-active');
}

// handle the display of analytics on the clicked influencer
function handleAnalytics(evt, $this) {

    evt.preventDefault();
    var $faIcon;

    var $influencer = $this
        .parents('.influencer');

    var $influencerContainer = $influencer
        .parent();

    var $analytics = $influencerContainer
        .parents('.row')
        .find('.influencer-analytics');

    if (($prevInfluencerClicked == null) || ($prevInfluencerClicked.index() != $influencerContainer.index())) {
        if ($analytics.css('display') == 'block') {
            $analytics.slideUp('slow', function() {
                $analytics
                    .insertAfter(selectorToAppendAnalytics($influencerContainer));

                drawAnalytics($influencerContainer);

                $analytics.slideDown('slow')
            });

            toggleSearchFaIcon($prevInfluencerClicked);
        }
        else {
            $analytics
                .insertAfter(selectorToAppendAnalytics($influencerContainer));

            drawAnalytics($influencerContainer);

            $analytics.slideDown('slow');
        }

        toggleSearchFaIcon($prevInfluencerClicked);
    }
    else {
        $analytics
                .insertAfter(selectorToAppendAnalytics($influencerContainer));

        $analytics.slideToggle('slow')
    }

    toggleActiveInfluencer($influencer);
    toggleSearchFaIcon($prevInfluencerClicked);

    $prevInfluencerClicked = $influencerContainer
}
