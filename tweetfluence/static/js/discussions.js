/**
 * Created by user on 1/22/2016.
 */

var g = {
        nodes: [],
        edges: []
    },
    prevWindowSize = 10000,
    prevInfluencerId = 0,
    s;

$(document).ready(function() {

    // Animate scrolling to graph section
    $("#draw-btn").on('click', function(evt) {

        evt.preventDefault();

        var topics = $('.tokenfield')
            .tokenfield('getTokensList')
            .split(', ');

        if (topics.length == 0 || topics == '') {
            $('.initial-graph-placeholder').slideDown('slow');
            $('#container').hide();
            return
        }
        else {
            $('.initial-graph-placeholder').slideUp('slow');
            $('#container').show();
        }

        $.ajax({
            type: "get",
            data: {'topics[]': topics },
            cache: false,
            url: 'spark/graphs/',
            dataType: "json",
            error: function (xhr, status, error) {
                console.log('An error has occured. ' + status);
            },
            success: function (response) {

                var influencersCreated = [],
                    topicsCreated = [],
                    topicColor,
                    $graphCanvas = $('#graph-canvas'),
                    $edgeColors = $('.edge-colors'),
                    g = {
                        nodes: [],
                        edges: []
                    };

                // Clear the previous chart & topics
                $graphCanvas.empty();
                $edgeColors.empty();

                $.each(response, function(i, data) {

                    // First Node-Influencer
                    if (influencersCreated.indexOf(data['connection'][0]) < 0) {
                        g.nodes.push({
                            id: 'n' + data['connection'][0],
                            x: Math.random(),
                            y: Math.random(),
                            size: '10',
                            color: '#666'

                        });

                        influencersCreated.push(data['connection'][0])
                    }
                    // Second Node-Influencer
                    if (influencersCreated.indexOf(data['connection'][1]) < 0) {
                        g.nodes.push({
                            id: 'n' + data['connection'][1],
                            x: Math.random(),
                            y: Math.random(),
                            size: '10',
                            color: '#666'

                        });

                        influencersCreated.push(data['connection'][1])
                    }

                    topicColor = '#' + intToRGB(hashCode(data['topic-name']));

                    // The connection between the two
                    g.edges.push({
                        id: 'e' + Math.random(),
                        source: 'n' + data['connection'][0],
                        target: 'n' + data['connection'][1],
                        size: '2',
                        color: topicColor
                    });

                    // Create a new topic on the right-sidebar
                    if (topicsCreated.indexOf(data['topic-name']) < 0) {

                        $edgeColors.append('<div class="margin-top-2 margin-bottom-2"> \
                            <div class="topic-color margin-right-4" style="background: ' + topicColor + '"></div> \
                            <div class="topic-name">' + data['topic-name'] + '</div> \
                            </div>');

                        topicsCreated.push(data['topic-name'])
                    }

                });

                // Instantiate sigma:
                s = new sigma({
                  graph: g,
                  container: 'graph-canvas'
                });

                s.settings({
                    enableCamera: false,
                    singleHover: true
                });

                s.bind('overNode', function(e) {
                    getNodeDetails(e)
                });

                $('html,body').animate({
                      scrollTop: $("#graph-section").offset().top
                }, 1500);
            }
        })
    });

    // Token and recommendation handlers
    $('#topics-filter')

        .on('tokenfield:createtoken', function (event) {

            var existingTokens = $(this).tokenfield('getTokens');

            $.each(existingTokens, function(index, token) {
                if (token.value === event.attrs.value)
                    event.preventDefault();
            });
        })

        .on('tokenfield:createdtoken', function (event) {
            handleTopicFilterOperation('create', event)
        })

        .on('tokenfield:removedtoken', function (event) {
            handleTopicFilterOperation('remove', event)
        })

        .tokenfield();


    // Change the order of elements for smaller devices
    $(window).on('resize load', function() {
        var currentWindowSize = window.innerWidth,
            $sectionContainer = $('#container').children('.row'),
            $edgeDetails = $sectionContainer.find('.edge-details');

        if ((currentWindowSize <= 991) && (prevWindowSize > 991)) {
            $($sectionContainer.children('div:first-child')).after($edgeDetails.detach())
        }
        else if ((currentWindowSize > 991) && (prevWindowSize <= 991)) {
            $sectionContainer.append($edgeDetails.detach())
        }

        prevWindowSize = currentWindowSize
    })
});

function handleTopicFilterOperation(operation, event) {

    var $topicRecommendationsContainer = $('.topic-recommendations'),
        token = event.attrs.value.toString(),
        tokenLowerCase = token.toLowerCase(),
        existingTokens = $(this).tokenfield('getTokens'),

        currentRecommendations = $topicRecommendationsContainer
            .find('.topic-recommendation')
            .map(function (i, el) {
                return $(el).text();
            }).get();

    if (tokenLowerCase in recommendations) {

        var topicsRecommended = recommendations[tokenLowerCase];

        if (operation == 'create') {

            $.each(topicsRecommended, function (index, recommendation) {
                if (currentRecommendations.indexOf(recommendation) < 0) {
                    $topicRecommendationsContainer
                        .append("<span class='topic-recommendation'>" + recommendation + "</span>")
                }
            });

            handleRecommendationClick();
        }
        else if (operation == 'remove') {

            $.each(topicsRecommended, function (index, recommendation) {
                if (currentRecommendations.indexOf(recommendation) >= 0) {
                    $(".topic-recommendation:contains(" + recommendation + ")")
                        .filter(function () {
                            return $(this).text() === recommendation;
                        })
                        .css('display', 'none')
                }
            })
        }
    }

    var visibleRecommendations = $topicRecommendationsContainer
            .find('.topic-recommendation')
            .map(function (i, el) {
                var $el = $(el);
                if ($el.css('display') != 'none')
                    return $el.text();
            }).get();

    if (visibleRecommendations.indexOf(token) >= 0) {
        $(".topic-recommendation:contains(" + token + ")")
            .filter(function () {
                return $(this).text() === token;
            })
            .css('display', 'none');

    }

    visibleRecommendations = $topicRecommendationsContainer
            .find('.topic-recommendation')
            .map(function (i, el) {
                var $el = $(el);
                if ($el.css('display') != 'none')
                    return $el.text();
            }).get();

    if ((visibleRecommendations.length == 0) || (existingTokens.length == 0))
        $topicRecommendationsContainer.slideUp('fast');
    else if ($topicRecommendationsContainer.css('display') == 'none')
            $topicRecommendationsContainer.slideDown('fast');

}

// Recommendation 'Click' Handler
function handleRecommendationClick() {

    $('.topic-recommendation').off().on('click', function (evt) {

        var $this = $(this),
            $topicsInput = $('#topics-filter'),
            recommendation = $this.text();

        $this.css('display', 'none');
        $topicsInput.tokenfield('createToken', recommendation);
    })
}

// Returns an arbitrary code for a random string
function hashCode(str) {
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
       hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
}

// Returns a colour based on the value of an arbitrary code
function intToRGB(i){
    var c = (i & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();

    return "00000".substring(0, 6 - c.length) + c;
}

function getNodeDetails(e) {

    var influencerId = e.data.node.id.replace('n','');

    if (prevInfluencerId == influencerId) return;

    $.ajax({
        type: "get",
        data: {},
        cache: false,
        url: 'spark/influencers/' +  influencerId,
        dataType: "json",
        error: function (xhr, status, error) {
            console.log('An error has occured. ' + status);
        },
        success: function (response) {

            var $nodeDetails = $('.node-details'),
                $influencerContainer = $nodeDetails.children('.influencer-container'),
                $topTopics = $influencerContainer.find('.influence-topic');

            $influencerContainer.fadeOut('slow', function() {

                $influencerContainer
                        .find('.influencer-img img')
                        .attr('src', response['twitter_image']);

                $influencerContainer
                        .find('.influencer-name')
                        .text(response['name']);

                $.each(response['top_topics'], function (i, response_topic) {
                    $($topTopics[i]).text(response_topic)

                })
            });

            $influencerContainer.fadeIn('slow');
             setTimeout(function (){ $influencerContainer.css('visibility', 'visible')}, 500);

            prevInfluencerId = influencerId
        }
    })
}


