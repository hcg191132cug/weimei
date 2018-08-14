$(document).ready(function(){
	$('.sm_container img').hover(function(){
		  $('#mid img').attr('src',$(this).attr('src').replace('small','mid'));
		  var l = $(this).attr('src').replace('small','big');
		  $('#retina').css({'background-image':"url("+l+")"});
		});
	/* This code is executed on the document ready event */
	var left	= 0,
		top		= 0,
		sizes	= { retina: { width:180, height:180}, mid:{ width:300, height:400 }, big:{width:600, height: 800} },
		mid	= $('#mid'),
		offset	= { left: mid.offset().left, top: mid.offset().top },
		retina	= $('#retina'),
		scaleW = (sizes.big.width)/sizes.mid.width,
		scaleH = (sizes.big.height)/sizes.mid.height;

	if(navigator.userAgent.indexOf('Chrome')!=-1)
	{
		/*	Applying a special chrome curosor,
			as it fails to render completely blank curosrs. */

		retina.addClass('chrome');
	}

	mid.mousemove(function(e){
		offset	= { left: mid.offset().left, top: mid.offset().top };
		left = (e.pageX-offset.left);
		top = (e.pageY-offset.top);
		if(retina.is(':not(:animated):hidden')){
			/* Fixes a bug where the retina div is not shown */
			mid.trigger('mouseenter');
		}

		if(left<0 || top<0 || left > sizes.mid.width || top > sizes.mid.height)
		{
			/*	If we are out of the bondaries of the
				mid screenshot, hide the retina div */

			if(!retina.is(':animated')){
				mid.trigger('mouseleave');
			}
			return false;
		}

		/*	Moving the retina div with the mouse
			(and scrolling the background) */
		/*改变mid的大小和背景大图的大小时要改变比例重新计算对应坐标*/
		var x = -scaleW*left+sizes.retina.width/2;
		var y = -scaleH*top+sizes.retina.height/2;
		retina.css({
			left				: left-sizes.retina.width/2,
			top					: top-sizes.retina.height/2,
			backgroundPosition	: (x)+'px '+(y)+'px'
		});

	}).mouseleave(function(){
		retina.stop(true,true).fadeOut('fast');
		retina.css('zIndex',0);
	}).mouseenter(function(){
		retina.css('zIndex',2);
		retina.stop(true,true).fadeIn('fast');
	});
});