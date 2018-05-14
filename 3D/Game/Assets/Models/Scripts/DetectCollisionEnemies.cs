using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DetectCollisionEnemies : MonoBehaviour {
 
    public Transform origin;                                    // target to aim for
    CharacterStats characterStats;
    CharacterStats playerStats;
    public float distance = 20f;

    void OnTriggerEnter(Collider col)
    {
        if (origin != null)
            distance = Vector3.Distance(origin.position, transform.position);

        if (col.gameObject.tag == "Player")
        {
            Debug.Log("Collision emeny with player");

            playerStats = col.gameObject.GetComponentInChildren<CharacterStats>();
            characterStats = origin.GetComponent<CharacterStats>();
            Stat enemyDamage = characterStats.damage;

            Debug.Log("Daño  " + enemyDamage.getValue());

       
            playerStats.TakeDamage(enemyDamage.getValue());

        }
    }
}
