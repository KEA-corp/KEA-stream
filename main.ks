# add kea_dep/Uf.kea

100 > random > $tofind

10 > LOOP

	"proposition: " > input > $user

	$tofind =- $user > IF
		"c est plus petit" > print
		END

	$tofind =+ $user > IF
		"c est plus grand" > print
		END
	
	$tofind =  $user > IF
		"bravo!" > print
		2 > BREAK
	END
