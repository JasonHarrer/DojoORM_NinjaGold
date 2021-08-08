$(document).ready(function() {
    $("input:radio[name=scenario]").click(onScenarioChange)
                
    onScenarioChange()
})

function onScenarioChange() {
    scenario = $("input:radio[name=scenario]:checked").val()
    console.log("scenario change: " + scenario)
    if (scenario == "amount") {
        $("#label-text-amount").text("gold")
    } else {
        $("#label-text-amount").text("turns")
    }
}
