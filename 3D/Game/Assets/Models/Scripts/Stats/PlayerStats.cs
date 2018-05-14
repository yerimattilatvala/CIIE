using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class PlayerStats : CharacterStats {

	private GameObject redLifeBar;
	private GameObject greenLifeBar;
	private int originalLife;
	public int buffTime;
	private int timeLeft;
	private GameObject dmgGUI;
	public Text timeText;

	void Start(){
		redLifeBar = GameObject.Find ("Canvas/RedHealth");
		greenLifeBar = GameObject.Find ("Canvas/GreenHealth");
		originalLife = maxHealth;
		dmgGUI = timeText.gameObject;
		dmgGUI.SetActive (false);
		timeLeft = buffTime;
	}

	void Update(){
		if (timeLeft >= 1) {
			timeText.text = ("Daño Aumentado: " + timeLeft);

		} else {
			dmgGUI.SetActive (false);
		}

	}

	void OnCollisionEnter(Collision collision){
		Debug.Log ("COLLISION ENTRANDO A ENANA");
	}

	public override void IncreaseHealth (int life)
	{
		base.IncreaseHealth (life);
		updateLifeBar (currentHealth);
	}

	public override void IncreaseDamage (int damage)
	{
		dmgGUI.SetActive (true);
		timeLeft = buffTime;
		StartCoroutine ("LoseTime");
		Time.timeScale = 1;

		base.IncreaseDamage (damage);
	}

	public override void TakeDamage (int damage)
	{
		base.TakeDamage (damage);
		updateLifeBar (currentHealth);
	}

	private void updateLifeBar(int life){
		if (life < 0) {
			life = 0;
		}
		float percentage = (float)life / (float)originalLife;
		if (percentage <= 0.5f) {
			greenLifeBar.transform.localScale = new Vector3 (0, 1, 1);
			redLifeBar.transform.localScale = new Vector3 (percentage * 2, 1, 1);
		} else {
			float percentageGreen = (float)(life - (originalLife / 2)) / (float)(originalLife / 2);
			greenLifeBar.transform.localScale = new Vector3 (percentageGreen,1, 1);
			redLifeBar.transform.localScale = new Vector3 (1, 1, 1);
		}


		
	}

	public override void Die ()
	{
		base.Die ();
		Debug.Log(transform.name + " died.");
	}


	IEnumerator LoseTime (){
		while (true) {
			yield return new WaitForSeconds (1);
			timeLeft--;
		}
	}
    
    
}
