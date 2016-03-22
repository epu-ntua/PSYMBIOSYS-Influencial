/**
 * Created by Aggelos on 12/28/2015.
 */

// Initialize the star ratings along with a dummy 3.5 star value
var $rating = $('.rating');
if ($rating.length) {

    $rating.rating({
        readonly: true,
        showClear: false,
        showCaption: false,
        size: 'xs'
    });

    $rating.rating('update', 3.5);
}

// Toggle the analytics section for an influencer

$('.toggle-analytics').on('click', function(evt) {

    var $influencerDiv = $(this)
        .parents('.influencer');

    var $analytics = $influencerDiv
        .find('.influencer-analytics');

    $('.influencer-analytics')
        .not($analytics)
        .hide('slow', function(){});

    $analytics
        .toggle('slow', function() {
            drawAveragesChart($influencerDiv, data);
            drawTimelineChart($influencerDiv, data2);
            //drawAnalytics($influencerDiv)
        })
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

    // Fetch all clicked Topics and insert them in a list
    var topic;
    var topics = [];
    var $checked = $('.topic-filter:checked');

    $.each($checked, function(i, checkbox) {
        topic = $(checkbox)
            .parents('.checkbox-tweetfluence')
            .find('.checkbox-text')
            .text();

        topics.push(topic)
    });

    // Fetch all Influencers and handle their display

    var $influencerDivs = $('.influencer');
    var $influenceTopics;

    $.each($influencerDivs, function(i, influencer) {
        $influenceTopics = $(influencer)
            .find('.influence-topics')
            .find('.influence-topic');

        handleInfluencerDisplay(influencer, $influenceTopics, topics);
    })
});

// Chart Draw
function drawAveragesChart($container, data) {

    var selector = '#' + $container.prop('id') + ' .averages-chart';

    if ($(selector).find('svg').length)
        return;

    var svg = dimple.newSvg(selector, "100%", "200px");
    var chart = new dimple.chart(svg, data['topics_averages']);

    chart.setBounds('50px', '20px', '80%', '75%');
    var x = chart.addCategoryAxis("x", "name");
    var y = chart.addMeasureAxis("y", "average_score");
    var series = chart.addSeries("name", dimple.plot.bar);
    x.title = '';
    y.title = 'Intensity';
    y.ticks = 6;
    x.fontSize = '6px';

    series.barGap = 0.6;
    chart.draw();

    $(window).on('resize', function () {
        chart.draw(0, true);
    });
}

function drawTimelineChart($container, data) {

    var selector = '#' + $container.prop('id') + ' .timeline-chart';

    if ($(selector).find('svg').length)
        return;

    var svg = dimple.newSvg(selector, "95%", "200px");
    var chart = new dimple.chart(svg, data['topics_values']);

    chart.setBounds('8%', '50px', '85%', '60%');
    var x =chart.addTimeAxis("x", "start", '%d %m %Y', '%b');
    var y = chart.addMeasureAxis("y", "score");
    var series = chart.addSeries("name", dimple.plot.line);

    x.title = '';
    y.title = '';
    y.ticks = 6;

    chart.addLegend('8%', '10px', '85%', '50px', 'left');
    chart.draw();

    $(window).on('resize', function () {
        chart.draw(0, true);
    });
}


function drawAnalytics($container) {

    var user = $container
        .find('.influencer-details div h2')
        .text();

    $.ajax({
        type: "get",
        data: {},
        cache: false,
        url: 'spark/influencers/' + user ,
        dataType: "json",
        error: function (xhr, status, error) {
            console.log('An error has occured. ' + status);
        },
        success: function (response) {
            drawAveragesChart($container, response);
            drawTimelineChart($container, response)
        }
    })
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

// Displays or hides the content of an Influencer
function triggerInfluencer(influencer, method) {

    var $influencer = $(influencer);

    if (method == 'show') {
        if ($influencer.css('display') == 'none')
            $influencer.slideDown();
    }
    else {
        if ($influencer.css('display') == 'block') {
            $influencer
                .slideUp(function() {
                    $(this)
                        .find('.influencer-analytics')
                        .hide()
            });
        }
    }
}

// Compares Topics and decides whether to display or hide an Influencer
function handleInfluencerDisplay(influencer, influencerTopics, filterTopics) {

    var topic;
    var noTopicMatch = true;

        $.each(influencerTopics, function(i, topicDiv){

            topic = $(topicDiv).text();

            if (inList(topic, filterTopics)) {
                triggerInfluencer(influencer, 'show');
                noTopicMatch = false;
                return false
            }
        });

    if (noTopicMatch)
        triggerInfluencer(influencer, 'hide')
}

// Dummy Data
var data ={topics_averages: [
    {
    name: 'Health',
    average_score: 1.21
    },
    {
        name: 'Fitness',
        average_score: 2.32
    },
    {
    name: 'Healfth',
    average_score: 1.21
    },
    {
        name: 'Ffitness',
        average_score: 2.32
    },
    {
    name: 'fswHealth',
    average_score: 1.21
    },
    {
        name: 'wdwwFitness',
        average_score: 2.32
    }
]};


var data2 ={topics_values: [
    {
    name: 'fitnless',
    score: 1.21,
    start: '11 12 2014'
    },
    {
        name: 'Fitness',
        score: 2.32,
        start: '15 12 2014'
    },
    {
    name: 'Health',
    score: 1.21,
    start: '31 12 2014'
    },
    {
        name: 'fitness',
        score: 4.32,
        start: '5 4 2015'
    },
    {
    name: 'Health',
    score: 3.21,
    start: '6 6 2015'
    },
    {
        name: 'Fitness',
        score: 3.32,
        start: '8 8 2015'
    }
]};


