using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DmgUpPotionController : MonoBehaviour {

	CharacterStats playerStats;
	public int dmgUp;
	private bool used;
	public int timeLeft=60;
	public Text timeText;

	void Start(){
		used = false;
	}

	void Update(){
		timeText.text = ("" + timeLeft);
	
	}



	void OnTriggerEnter(Collider col)
	{

		if (col.gameObject.tag == "Player") {
			if (used)
				return;
			else {
				used = true;

			Debug.Log ("Consumir pocion Daño");
			StartCoroutine ("LoseTime");
			Time.timeScale = 1;
			Destroy (this.gameObject);
			playerStats = col.gameObject.GetComponentInChildren<CharacterStats> ();
			playerStats.IncreaseDamage (dmgUp);


			} 
		}
	}


	IEnumerator LoseTime (){
		while (true) {
			yield return new WaitForSeconds (1);
			timeLeft--;
		}
	}
}
