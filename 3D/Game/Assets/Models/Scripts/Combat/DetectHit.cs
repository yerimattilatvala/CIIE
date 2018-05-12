using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DetectHit : MonoBehaviour {
	CharacterStats enemyStats;
	CharacterStats playerStats;
	float timer=0.0f;
	public float invulnerability=1.0f;


	void OnTriggerEnter(Collider col){

		if (col.gameObject.tag == "hitMarker")
		{
			print ("COLL");
			if (((EnemyAttackTimer)col.gameObject.GetComponent(typeof(EnemyAttackTimer))).canAttack()){
				print ("ATTACK");
				playerStats = this.gameObject.GetComponentInChildren<CharacterStats> ();
				enemyStats = col.gameObject.GetComponentInParent<CharacterStats> ();
				Stat enemyDamage = enemyStats.damage;
				playerStats.TakeDamage (enemyDamage.getValue ());
			}
			/*if (timer >= invulnerability) {
				playerStats = this.gameObject.GetComponentInChildren<CharacterStats> ();
				enemyStats = col.gameObject.GetComponentInParent<CharacterStats> ();
				Stat enemyDamage = enemyStats.damage;
				playerStats.TakeDamage (enemyDamage.getValue ());
				timer = 0.0f;
			}*/
		}
	}

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {		
		timer += Time.deltaTime;
	}
}
