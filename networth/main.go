package main

import (
    "fmt"
    "net/http"
    "os"

    "github.com/gin-gonic/gin"
    "github.com/DuckySoLucky/SkyCrypt-Types"
    "github.com/SkyCryptWebsite/SkyHelper-Networth-Go"
)

func main() {
    router := gin.New()
    router.Use(gin.Recovery())
    router.POST("/networth", getNetworth)
    router.GET("/healthz", func(c *gin.Context) {
        c.IndentedJSON(http.StatusOK, gin.H{"success": true})
    })
    router.Run(os.Getenv("ADDRESS"))  // Defaults to "0.0.0.0:8080" if ADDRESS not set
}

func getNetworth(c *gin.Context) {
    var payload struct {
        UserProfile *skycrypttypes.Member `json:"profile" binding:"required"`
        MuseumData  *skycrypttypes.Museum `json:"museum"  binding:"required"`
        BankBalance float64               `json:"balance" binding:"required"`
    }

    if err := c.ShouldBindJSON(&payload); err != nil {
        c.IndentedJSON(http.StatusBadRequest, gin.H{
            "success": false,
            "error": fmt.Sprintf("Invalid request body: %v", err),
        })
        return
    }

    calculator, err := skyhelpernetworthgo.NewProfileNetworthCalculator(payload.UserProfile, payload.MuseumData, payload.BankBalance)
	if err != nil {
		c.IndentedJSON(http.StatusInternalServerError, gin.H{
		    "success": false,
			"error": fmt.Sprintf("Failed to create networth calculator: %v", err),
		})
        return
	}
    nonCosmeticNetworth := calculator.GetNonCosmeticNetworth(skyhelpernetworthgo.NetworthOptions{OnlyNetworth: true})

    c.IndentedJSON(http.StatusOK, gin.H{
        "success": true,
        "non_cosmetic_networth": nonCosmeticNetworth.Networth,
    })
}
