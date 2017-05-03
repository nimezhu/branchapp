var branch = branch || {};
(function(B){
  var ncolor = {
    "A": 4,
    "a": 4,
    "C": 1,
    "c": 1,
    "G": 2,
    "g": 2,
    "T": 3,
    "t": 3
  }
  var color = d3.scaleOrdinal(d3.schemeCategory10).domain([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]);
  var ncolors = function(n) {
    if (ncolor[n]) {
      return color(ncolor[n]);
    } else {
      return "grey";
    }
  }
    B.chart = function() {
    var height = 200;
    var width = 10;
    var chart = function(selection) {
      selection.each(function(d, i) {
        if (!d.result) {
          return
        }
        var scale = d3.scaleLinear().range([height, 0]);
        var minY = d3.min(d.result)
        var maxY = d3.max(d.result)
        scale.domain([minY, maxY])
        if (d.v) {
          d3.select(this).selectAll(".v").data(d.v).enter().append("text")
            .attr("class", "v")
            .attr("x", function(d) {
              return (d[0] - 10) * width
            })
            .attr("y", function(d1) {
              var e = d.result[d1[0] - 10]
              if (e > 0) {
                return scale(e)
              } else {
                return scale(e) + 10
              }
            })
            //.attr("y",20)
            .text("*")
        }
        d3.select(this).selectAll("rect").data(d.result).enter()
          .append("rect")
          .attr("x", function(d, i) {
            return i * width
          })
          .attr("y", function(d, i) {
            return scale(Math.max(0, d))
          })
          .attr("height", function(d, i) {
            return Math.abs(scale(d) - scale(0))
          })
          .attr("width", width - 2)
          .attr("fill", function(d0, i) {
            return ncolors(d.seq[i + 5])
          })
          .append("title")
          .text(function(d0, i) {
            return d.seq[i + 5] + ":" + (i - 50) + ":" + (Math.round(d0 * 100) / 100)
          })
        d3.select(this).append("text")
          .attr("x", -30)
          .attr("y", scale(0) + 5)
          .text("-50")
        d3.select(this).append("text")
          .attr("x", 40 * width)
          .attr("y", scale(0) + 5)
          .text("-11")
        var yAxis = d3.axisRight()
          .scale(scale)

        var yG = d3.select(this).append("g").attr("transform", "translate(" + (40 * width + 30) + ")")
          .call(yAxis);
        var l = d3.select(this).append("g").attr("transform", "translate(" + 40 * width + ",20)")
          .selectAll("g").data(["A", "C", "G", "T"]).enter()
          .append("g").attr("transform", function(d, i) {
            return "translate(5," + i * 20 + ")"
          })
          .append("text")
          .text(function(d, i) {
            return d
          })
          .attr("fill", function(d, i) {
            return ncolors(d)
          })

      });
    }
    return chart;
  }

  var h = {
  	"A":"T",
  	"a":"t",
  	"C":"G",
  	"c":"g",
  	"G":"C",
  	"g":"c",
  	"T":"A",
  	"t":"a",
  	"N":"N",
  	"n":"n"
  }
  var rc = function(seq) {
  	var s=seq.split('')
  	var r=[];
  	s.reverse().forEach(function(d) {
  		r.push(h[d])
  	})
  	return r.join('');
  }
  B.getseq = function(i,callback) {
  	$.ajax( {
  		url:"http://genome.ucsc.edu/cgi-bin/das/hg19/dna?segment="+i.chr+":"+(i.start+1)+","+i.end,
  		dataType:"xml",
  		success: function(d) {
  			var seq=$(d).find("DNA:first").text().replace(/\s/g,'')
        console.log("xml",d)
        console.log("seq in",seq);
        console.log("i in",i)
  			if(i.strand=="-") {i.seq=rc(seq)}
  			else {
  				i.seq=seq;
  			}
  			callback(i);
  		}
  	  }
  	 )
  	}

})(branch)
